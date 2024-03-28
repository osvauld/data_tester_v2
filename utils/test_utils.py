import uuid

from dateutil.parser import parse


def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
    except ValueError:
        return False

    # Check if it's not all zeros
    return uuid_obj != uuid.UUID("00000000-0000-0000-0000-000000000000")


def is_valid_timestamp(timestamp_string):
    try:
        parse(timestamp_string)
        return True
    except ValueError:
        return False
