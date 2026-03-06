import factory
from factory.django import DjangoModelFactory

from config.roles import Role
from modules.user.models import User


DEFAULT_PASSWORD = "TestPass123!"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    role = Role.STAFF
    is_active = True
    password = DEFAULT_PASSWORD

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", DEFAULT_PASSWORD)
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, password=password, **kwargs)
