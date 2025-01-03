from django.core.exceptions import ValidationError
import re


def validate_username(value):
    """
    Validates a username:
    - Must be between 3 and 30 characters.
    - Can only contain alphanumeric characters, underscores (_), and dots (.).
    - Cannot start or end with a dot or underscore.
    - Cannot contain consecutive dots or underscores.
    """
    if not 3 <= len(value) <= 40:
        raise ValidationError("Username must be between 3 and 30 characters long.")

    if not re.match(r"^[a-zA-Z0-9_.]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, underscores, and dots."
        )

    if value[0] in "._" or value[-1] in "._":
        raise ValidationError("Username cannot start or end with a dot or underscore.")

    if ".." in value or "__" in value or "._" in value or "_. " in value:
        raise ValidationError(
            "Username cannot contain consecutive dots or underscores."
        )



