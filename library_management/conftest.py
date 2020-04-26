import pytest
from library_management import settings
from rest_framework.test import APIClient

from library_management.users.models import UserType
from library_management.users.tests.factories import UserFactory


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ':memory:',
    }


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def member(db):
    return UserFactory()


@pytest.fixture
def admin(db):
    return UserFactory(user_type=UserType.ADMIN)


@pytest.fixture
def member_auth_client(member, client):
    client.force_authenticate(member)
    return client


@pytest.fixture
def admin_auth_client(admin, client):
    client.force_authenticate(admin)
    return client
