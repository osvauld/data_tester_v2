from model.credential import Credential, Field, UserFields
from factories.user import UserFactory
import factory

import uuid


class FieldFactory(factory.Factory):
    class Meta:
        model = Field

    field_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    field_name = factory.Faker("word")
    field_value = factory.Faker("password")
    field_type = factory.Faker(
        "random_element", elements=["sensitive", "non-sensitive"]
    )


class UserFieldsFactory(factory.Factory):
    class Meta:
        model = UserFields

    user = factory.SubFactory(UserFactory)
    fields = factory.List(factory.SubFactory(FieldFactory) for _ in range(3))


class CredentialFactory(factory.Factory):
    class Meta:
        model = Credential

    credential_id = factory.Faker("uuid4")
    name = factory.Faker("company")
    folder_id = factory.Faker("uuid4")
    user = factory.SubFactory(UserFactory)
    description = factory.Faker("text")
    credential_type = factory.Faker("random_element", elements=["login", "other"])
    user_fields = factory.List(factory.SubFactory(UserFieldsFactory) for _ in range(3))
    access_type = factory.Faker("random_element", elements=["owner", "write", "read"])
