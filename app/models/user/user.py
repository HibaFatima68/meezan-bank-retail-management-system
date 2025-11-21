from app.db_utils import UserDAO, BeneficiaryDAO
import re

User = UserDAO
Beneficiary = BeneficiaryDAO

def insert_hyphens(value):
    """Format card number with hyphens"""
    value = re.sub(r'\s', '', value)
    return re.sub(r'\d{4}(?!$)', r'\g<0>-', value)
