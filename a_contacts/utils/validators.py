import os
from django.core.exceptions import ValidationError


def validate_csv_file_extension(value):
    allowed_extensions = ['.csv'] 
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(
            f'Unsupported file: {value.name}. Only .csv files are allowed.')
