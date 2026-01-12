"""
Custom validators
"""
import re
from wtforms.validators import ValidationError


def validate_korean_phone(form, field):
    """Validate Korean phone number format"""
    if field.data:
        # Korean phone format: 010-1234-5678 or 02-1234-5678
        pattern = r'^0\d{1,2}-\d{3,4}-\d{4}$'
        if not re.match(pattern, field.data):
            raise ValidationError('올바른 전화번호 형식이 아닙니다. (Invalid phone number format)')


def validate_business_registration(form, field):
    """Validate Korean business registration number"""
    if field.data:
        # Remove hyphens
        number = field.data.replace('-', '')

        if len(number) != 10:
            raise ValidationError('사업자등록번호는 10자리여야 합니다. (Business registration must be 10 digits)')

        if not number.isdigit():
            raise ValidationError('사업자등록번호는 숫자만 포함해야 합니다. (Business registration must contain only numbers)')


def validate_positive_number(form, field):
    """Validate that number is positive"""
    if field.data is not None and field.data < 0:
        raise ValidationError('양수여야 합니다. (Must be a positive number)')


def validate_non_negative_number(form, field):
    """Validate that number is non-negative"""
    if field.data is not None and field.data < 0:
        raise ValidationError('0 이상이어야 합니다. (Must be non-negative)')


def validate_percentage(form, field):
    """Validate percentage (0-100)"""
    if field.data is not None:
        if field.data < 0 or field.data > 100:
            raise ValidationError('0에서 100 사이의 값이어야 합니다. (Must be between 0 and 100)')
