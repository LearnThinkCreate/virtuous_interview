# AUTOGENERATED! DO NOT EDIT! File to edit: ../04_Test.ipynb.

# %% auto 0
__all__ = ['final_contacts', 'final_contact_methods', 'final_gifts', 'missing_no_required_fields', 'email_is_valid',
           'number_is_valid', 'zip_is_valid', 'test_contacts_columns', 'test_gifts_columns',
           'test_contact_method_columns', 'test_contact_required_fields', 'test_contacts_contact_type',
           'test_contact_email', 'test_contact_phone_number_valid', 'test_contact_valid_zip',
           'test_gift_required_fields', 'test_gift_amount_is_float', 'test_contact_method_required_fields',
           'test_contact_method_type']

# %% ../04_Test.ipynb 2
import pandas as pd
import re
from .utils import valid_email, validate_us_phone_number
from .solution_pd import postal_code_pattern

# %% ../04_Test.ipynb 3
final_contacts = pd.read_csv('data/final_contacts.csv').fillna('')
final_contact_methods = pd.read_csv('data/final_contact_methods.csv').fillna('')
final_gifts = pd.read_csv('data/final_gifts.csv').fillna('')

# %% ../04_Test.ipynb 5
def missing_no_required_fields(df: pd.DataFrame, columns: list):
    for column in columns:
        assert ~(df[column] == '').any(), f"Missing values found in column '{column}'"


# %% ../04_Test.ipynb 6
def email_is_valid(s):
    if s == '':
        return True
    return valid_email(s)

# %% ../04_Test.ipynb 7
def number_is_valid(s):
    if s == '':
        return True
    elif validate_us_phone_number(s) == '':
        return False
    else:
        return True

# %% ../04_Test.ipynb 8
def zip_is_valid(p):
    s = str(p).replace('.0', '')
    if s == '':
        return True
    else:
        return bool(re.match(postal_code_pattern, s))

# %% ../04_Test.ipynb 11
def test_contacts_columns():
    assert final_contacts.columns.tolist() == [
    'LegacyContactId', 'LegacyIndividualId', 'ContactType', 'ContactName',
    'FirstName', 
    'LastName', 'SecondaryLegacyIndividualId', 'SecondaryFirstName',
    'SecondaryLastName', 'HomePhone', 'HomeEmail', 'Address1', 
    'City', 'State', 'PostalCode', 'IsPrivate', 'IsDeceased',
    ]

# %% ../04_Test.ipynb 14
def test_gifts_columns():
    assert final_gifts.columns.tolist() == ['LegacyContactId', 'LegacyGiftId', 'GiftType', 'GiftDate',
           'GiftAmount', 'Notes', 'CreditCardType', 'Project1Code',
           'Project2Code', 'LegacyPledgeID']

# %% ../04_Test.ipynb 17
def test_contact_method_columns():
    assert final_contact_methods.columns.tolist() == ['LegacyContactId', 'Type', 'Value']

# %% ../04_Test.ipynb 21
def test_contact_required_fields():
    missing_no_required_fields(final_contacts, ['LegacyContactId', 'LegacyIndividualId', 'ContactType', 'FirstName', 'LastName'])

# %% ../04_Test.ipynb 24
def test_contacts_contact_type():
    assert final_contacts.ContactType.isin(['Household', 'Organization']).all()

# %% ../04_Test.ipynb 27
def test_contact_email():
    assert final_contacts.HomeEmail.apply(email_is_valid).all()

# %% ../04_Test.ipynb 30
def test_contact_phone_number_valid():
    assert final_contacts.HomePhone.apply(number_is_valid).all()

# %% ../04_Test.ipynb 33
def test_contact_valid_zip():
    assert final_contacts.PostalCode.apply(zip_is_valid).all()

# %% ../04_Test.ipynb 40
def test_gift_required_fields():
    missing_no_required_fields(final_gifts, ['LegacyContactId', 'LegacyGiftId', 'GiftType', 'GiftDate', 'GiftAmount', 'LegacyPledgeID'])

# %% ../04_Test.ipynb 46
# Assert final_gifts['GiftAmount'] is a float
def test_gift_amount_is_float():
    assert final_gifts['GiftAmount'].dtype == 'float64'

# %% ../04_Test.ipynb 56
def test_contact_method_required_fields():
    missing_no_required_fields(final_contact_methods, ['LegacyContactId', 'Type', 'Value'])

# %% ../04_Test.ipynb 59
def test_contact_method_type():
    assert final_contact_methods.Type.isin(['HomePhone', 'HomeEmail', 'Fax']).all()
