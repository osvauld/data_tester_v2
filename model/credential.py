import uuid


from model.user import User


class Field:
    def __init__(
        self,
        field_name,
        field_value=None,
        field_type=None,
        field_id=None,
    ):
        self.field_id = field_id
        self.field_name = field_name
        self.field_value = field_value
        self.field_type = field_type

    def __eq__(self, other):

        if not isinstance(other, Field):
            return NotImplemented

        return (
            self.field_name == other.field_name
            and self.field_value == other.field_value
            and self.field_type == other.field_type
        )

    @classmethod
    def from_dict(cls, field_dict):
        return cls(
            field_id=field_dict["id"],
            field_name=field_dict["fieldName"],
            field_value=field_dict["fieldValue"],
            field_type=field_dict["fieldType"],
        )


class UserFields:
    def __init__(self, user: User, fields: list[Field]):
        self.user = user
        self.fields = fields


class Credential:
    def __init__(
        self,
        name: str,
        folder_id: uuid.UUID,
        user: User,
        description: str = None,
        credential_type: str = None,
        user_fields: list[UserFields] = None,
        credential_id: uuid.UUID = None,
        access_type: str = None,
    ):
        self.name = name
        self.folder_id = folder_id
        self.user = user
        self.credential_id = credential_id
        self.description = description
        self.credential_type = credential_type
        self.access_type = access_type

        if user_fields is None:
            self.user_fields = []
        else:
            self.user_fields = user_fields
