# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_Setup.ipynb.

# %% auto 0
__all__ = ['contact_methods', 'contacts', 'gifts', 'int_cols', 'donors_not_in_contacts', 'records_to_join', 'id',
           'blank_name_records', 'blank_name_numbers', 'gift_name_records', 'project_codes', 'to_camel_case',
           'transform_cnames', 'classify_phone_email', 'set_contact_name', 'custom_parser', 'valid_email', 'fix_email',
           'validate_us_phone_number']

# %% ../00_Setup.ipynb 3
from nbdev.showdoc import *
import pandas as pd
import re

# %% ../00_Setup.ipynb 4
contact_methods = pd.read_csv('data/contact_methods.csv').fillna('')
contacts = pd.read_csv('data/contacts.csv').fillna('')
gifts = pd.read_csv('data/gifts.csv').fillna('')

# %% ../00_Setup.ipynb 10
def to_camel_case(s):
    """Converts a string to camel case."""
    # Remove all non-alphanumeric characters and replace with a space
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)

    # Split by space and capitalize the first letter of each word
    words = s.split()
    return ''.join(word.capitalize() for word in words)

# %% ../00_Setup.ipynb 17
def transform_cnames(df, func=to_camel_case):
    """Apply a function to all column names of a dataframe.
    It may not always be the case that I want to apply to_camel_case as the column transformation function.
    Because of this func is an optional argument with a default value of to_camel_case  
    """
    df.columns = df.columns.map(func)
    return None

# %% ../00_Setup.ipynb 19
for df in [contact_methods, contacts, gifts]:
    transform_cnames(df)

# %% ../00_Setup.ipynb 24
int_cols = ['GiftId', 'PledgeNumber']

# %% ../00_Setup.ipynb 25
gifts[int_cols] = gifts[int_cols].replace({'': 0}).astype(int)

# %% ../00_Setup.ipynb 27
gifts['AmountReceived'] = gifts.AmountReceived.apply(
    lambda x: float(re.sub(r'[^a-zA-Z0-9\.-]', '', x)))

# %% ../00_Setup.ipynb 31
gifts.loc[gifts.PledgeNumber == 0,
          'PledgeNumber'] = gifts[gifts.PledgeNumber == 0].index
gifts.loc[gifts.GiftId == 0, 'GiftId'] = gifts[gifts.GiftId == 0].index

# %% ../00_Setup.ipynb 34
gifts = gifts.rename(
    columns={'PledgeNumber': 'LegacyPledgeID', 'GiftId': 'LegacyGiftId'})

# %% ../00_Setup.ipynb 38
def classify_phone_email(value):
    """Classify a value as a phone number, email, or None."""
    if "@" in value:
        return "email"
    if re.search(r'\d{3}-\d{3}-\d{4}', value):
        return "phone"
    return None

# %% ../00_Setup.ipynb 47
for index, row in contacts.iterrows():
    phone_classification = classify_phone_email(row['Phone'])
    email_classification = classify_phone_email(row['EMail'])

    if phone_classification == "email":
        contacts.at[index, 'EMail'] = row['Phone']
        contacts.at[index, 'Phone'] = ''

    if email_classification == "phone":
        contacts.at[index, 'Phone'] = row['EMail']
        contacts.at[index, 'EMail'] = ''

# %% ../00_Setup.ipynb 56
donors_not_in_contacts = gifts.loc[~gifts.DonorNumber.isin(
    contacts.Number.unique()), :]

# %% ../00_Setup.ipynb 59
contacts = pd.concat([
    contacts,
    # Dataframe of donors not in contacts
    pd.DataFrame(donors_not_in_contacts[['DonorNumber', 'FirstName', 'LastName']]
                 .drop_duplicates()
                 .rename(columns={'DonorNumber': 'Number'})
                 .drop_duplicates()
                 .to_dict('records'))
])

# %% ../00_Setup.ipynb 63
contacts[['FirstName', 'SecondaryFirstName']] = contacts['FirstName'].str.split(
    ' & | and ', expand=True).fillna('')

# %% ../00_Setup.ipynb 65
records_to_join = contacts.loc[contacts.Number.duplicated(), :].to_dict(
    orient='records')

# %% ../00_Setup.ipynb 67
contacts = contacts.loc[~contacts.Number.duplicated(), :]

# %% ../00_Setup.ipynb 69
for record in records_to_join:
    contacts.loc[contacts.Number.isin([record['Number']]), [
        'SecondaryFirstName', 'SecondaryLastName']] = [record['FirstName'], record['LastName']]

# %% ../00_Setup.ipynb 70
contacts['SecondaryLastName'] = contacts.SecondaryLastName.fillna('')

# %% ../00_Setup.ipynb 72
contacts['SecondaryLastName'] = contacts.apply(
    lambda x: x['LastName'] if x['SecondaryLastName'] == '' and x['SecondaryFirstName'] != '' else x['SecondaryLastName'], axis=1)

# %% ../00_Setup.ipynb 75
contacts[['LegacyIndividualId', 'SecondaryLegacyIndividualId']] = None

# %% ../00_Setup.ipynb 76
contacts.reset_index(inplace=True, drop=True)

# %% ../00_Setup.ipynb 78
id = 0
for index, row in contacts.iterrows():
    contacts.loc[index, 'LegacyIndividualId'] = id
    id += 1
    if row['SecondaryFirstName'] != '':
        contacts.loc[index, 'SecondaryLegacyIndividualId'] = id
        id += 1

# %% ../00_Setup.ipynb 79
contacts.fillna('', inplace=True)

# %% ../00_Setup.ipynb 82
blank_name_records = ((contacts.FirstName == '') | (contacts.LastName == ''))

# %% ../00_Setup.ipynb 86
blank_name_numbers = contacts.loc[blank_name_records, 'Number']

# %% ../00_Setup.ipynb 89
gift_name_records = gifts.loc[gifts.DonorNumber.isin(
    blank_name_numbers), ['DonorNumber', 'FirstName', 'LastName']].drop_duplicates()

# %% ../00_Setup.ipynb 91
gift_name_records = gift_name_records.loc[(
    (gift_name_records.FirstName != '') & (gift_name_records.LastName != '')), :]
gift_name_records

# %% ../00_Setup.ipynb 93
for _, row in gift_name_records.iterrows():
    contacts.loc[contacts['Number'] == row['DonorNumber'], [
        'FirstName', 'LastName']] = [row['FirstName'], row['LastName']]

# %% ../00_Setup.ipynb 99
def set_contact_name(row):
    """Sets the contact name for a given row in the dataframe."""
    if row['LastName'] == row['SecondaryLastName']:
        return row['FirstName'] + ' & ' + row['SecondaryFirstName'] + ' ' + row['LastName']
    elif row['SecondaryFirstName'] != '':
        return row['FirstName'] + ' ' + row['LastName'] + ' & ' + row['SecondaryFirstName'] + ' ' + row['SecondaryLastName']
    else:
        return row['FirstName'] + ' ' + row['LastName']

# %% ../00_Setup.ipynb 100
contacts['ContactName'] = contacts.apply(set_contact_name, axis=1)

# %% ../00_Setup.ipynb 105
project_codes = gifts.FundId.str.split(', ', expand=True)

# %% ../00_Setup.ipynb 108
gifts[['Project1Code', 'Project2Code']] = project_codes

# %% ../00_Setup.ipynb 110
gifts = gifts.loc[:, gifts.columns.drop('FundId')].copy()

# %% ../00_Setup.ipynb 114
from datetime import datetime

# %% ../00_Setup.ipynb 115
def custom_parser(date_str):
    """Parses a date string into a datetime object."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return datetime.strptime(date_str, '%Y/%m/%d')

# %% ../00_Setup.ipynb 120
gifts['GiftDate'] = gifts['Date'].apply(custom_parser)

# %% ../00_Setup.ipynb 122
gifts = gifts.loc[:, gifts.columns.drop('Date')].copy()

# %% ../00_Setup.ipynb 127
def valid_email(s):
    """Validates an email address."""
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if pattern.match(s):
        return True
    return False

# %% ../00_Setup.ipynb 135
def fix_email(email):
    """Fixes common mistakes in email addresses."""
    if not email:
        return ''

    email = re.sub(r'\s', '', email)

    # Check and fix common mistakes in top-level domain (TLD)
    for wrong_tld, correct_tld in [('co', 'com'), ('cmo', 'com'), ('con', 'com')]:
        if email.endswith('.' + wrong_tld):
            email = email[:-len(wrong_tld)] + correct_tld

    # Check and fix common mistakes in domain names
    for wrong_domain, correct_domain in [('gmial', 'gmail'), ('yahho', 'yahoo')]:
        email = email.replace('@' + wrong_domain, '@' + correct_domain)

    if valid_email(email):
        return email

    return ''

# %% ../00_Setup.ipynb 146
contacts['EMail'] = contacts.EMail.apply(fix_email)

# %% ../00_Setup.ipynb 151
def validate_us_phone_number(phone_number):
    """Validates a US phone number and returns it if valid, otherwise returns an empty string."""
    # Patterns for different US phone number formats
    patterns = [
        r'^\+1\s?\d{3}-\d{3}-\d{4}$',
        r'^\(\d{3}\)\s?\d{3}-\d{4}$',
        r'^\d{3}-\d{3}-\d{4}$',
        r'^\d{3}-\d{4}$'
    ]

    # Check if the phone number matches any of the patterns
    for pattern in patterns:
        if re.match(pattern, phone_number):
            return phone_number

    # Checking if the string contains only numbers and is of length 7 or 10
    numeric_string = re.sub('[^0-9]', '', phone_number)
    length = len(numeric_string)
    if length == 7 or length == 10:
        return phone_number

    return ''

# %% ../00_Setup.ipynb 165
contacts['Phone'] = contacts.Phone.apply(validate_us_phone_number)

# %% ../00_Setup.ipynb 166
contacts.fillna('', inplace=True)
