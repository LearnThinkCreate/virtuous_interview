# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_Pandas_Solution.ipynb.

# %% auto 0
__all__ = ['validate_mastercard', 'validate_amex', 'validate_visa', 'validate_discover', 'validate_credit_card', 'postal_code_pattern', 'temp_contacts', 'temp_contact_methods', 'contacts_wide', 'clean_payment_type']

# %% ../02_Pandas_Solution.ipynb 2
import pandas as pd
import numpy as np
import re

from .utils import contacts, contact_methods, gifts

# %% ../02_Pandas_Solution.ipynb 29
def validate_mastercard(string):
    # Match strings that contain "mastercard" or "master card", case insensitive
    pattern = r'master\s?card'
    return bool(re.search(pattern, string, re.IGNORECASE))

def validate_amex(string):
    # Match strings that contain "amex", "american express", or "american ex", case insensitive
    pattern = r'amex|american\s?express|american\s?ex'
    return bool(re.search(pattern, string, re.IGNORECASE))

def validate_visa(string):
    # Match strings that contain "visa", case insensitive
    pattern = r'visa'
    return bool(re.search(pattern, string, re.IGNORECASE))

def validate_discover(string):
    # Match strings that contain "discover", case insensitive
    pattern = r'discover'
    return bool(re.search(pattern, string, re.IGNORECASE))

def validate_credit_card(string): 
    if validate_mastercard(string):
        return 'Mastercard'
    elif validate_amex(string):
        return 'AMEX'
    elif validate_visa(string):
        return 'Visa'
    elif validate_discover(string):
        return 'Discover'
    else:
        return ''

# %% ../02_Pandas_Solution.ipynb 30
gifts['CreditCardType'] = gifts.CreditCardType.apply(validate_credit_card)

# %% ../02_Pandas_Solution.ipynb 10
contacts['ContactType'] = contacts.apply(lambda x: 'Household' if x['CompanyName'] == '' else 'Organization', axis=1)

# %% ../02_Pandas_Solution.ipynb 14
postal_code_pattern = '[0-9]{5}(?:-[0-9]{4})?$'

# %% ../02_Pandas_Solution.ipynb 15
contacts['Postal'] = contacts.Postal.apply(lambda x: x if re.match(postal_code_pattern, x) else '')

# %% ../02_Pandas_Solution.ipynb 19
contacts['Deceased'] = contacts.Deceased.apply(lambda x: True if x == 'Yes' else False)

# %% ../02_Pandas_Solution.ipynb 23
def clean_payment_type(row):
    payment_method = ''
    orginal_payment_method = str(row['PaymentMethod']).lower()
    
    if row['AmountReceived'] < 0:
        payment_method = 'Reversing Transaction'
    elif re.match('credit', orginal_payment_method):
        payment_method = 'Credit'
    elif orginal_payment_method in ['check', 'cash', 'reversing transaction']:
        payment_method = orginal_payment_method.title()
    else:
        payment_method = 'Other'

    return payment_method

# %% ../02_Pandas_Solution.ipynb 24
gifts['PaymentMethod'] = gifts.apply(clean_payment_type, axis=1)

# %% ../02_Pandas_Solution.ipynb 35
temp_contacts = contacts[['Number', 'Phone', 'EMail']].rename(columns={
    'Number': 'LegacyContactId',
    'Phone': 'HomePhone',
    'EMail': 'HomeEmail'
}).copy()

# %% ../02_Pandas_Solution.ipynb 36
temp_contact_methods = contact_methods.rename(columns={'DonorNumber':'LegacyContactId'})

# %% ../02_Pandas_Solution.ipynb 37
contacts_wide = temp_contacts.merge(temp_contact_methods,
                                how='left',
                                on='LegacyContactId',
                                ).sort_values('LegacyContactId')