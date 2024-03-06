import factory

from model.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    user_id = factory.Faker("uuid4")
    name = factory.Faker("name")
    username = factory.Faker("user_name")
