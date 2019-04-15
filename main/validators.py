from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_no_plus_in_email(value):
    if isinstance(value, str) and '+' in value:
        raise ValidationError(_('Поле email не должно содержать +'))
