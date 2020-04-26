import pytest
import factory
from django.urls import reverse

from .factories import fake, User, UserFactory
from ..models import UserType


class TestRegistration:
    url = reverse("v1:users:rest_register")
    test_password = "test_pass"

    @pytest.fixture
    def register_data(self):
        data = {
            'email': fake.email(),
            'password1': self.test_password,
            'password2': self.test_password,
            'user_type': UserType.MEMBER,
        }
        return data

    def test_user_registration_success(self, client, register_data, db):
        request = client.post(self.url, register_data)
        user = User.objects.filter(id=request.data["user"]["id"], is_active=True)

        assert request.status_code == 201
        assert user.exists()
        assert user[0].check_password(self.test_password)

    def test_password_mismatch(self, client, register_data, db):
        register_data["password2"] = fake.word()

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_unique_email(self, client, register_data, db):
        UserFactory(email=register_data["email"])

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_cant_create_admin_user_when_not_logged_in(self, client, register_data, db):
        register_data['user_type'] = UserType.ADMIN
        request = client.post(self.url, register_data)
        assert request.status_code == 400
        assert request.json()["user_type"][0] == "Only an admin user can create another admin!"
        user_exists = User.objects.filter(email=register_data['email']).exists()
        assert user_exists is False

    def test_member_cant_create_admin(self, member_auth_client, register_data, db):
        register_data['user_type'] = UserType.ADMIN
        request = member_auth_client.post(self.url, register_data)
        assert request.status_code == 400
        assert request.json()["user_type"][0] == "Only an admin user can create another admin!"
        user_exists = User.objects.filter(email=register_data['email']).exists()
        assert user_exists is False

    def test_create_admin(self, admin_auth_client, register_data, db):
        register_data['user_type'] = UserType.ADMIN
        request = admin_auth_client.post(self.url, register_data)
        assert request.status_code == 201


class TestLogin:

    url = reverse("v1:users:rest_login")
    password = "test_pass"

    def test_login(self, member, client):

        assert member.check_password(self.password)

        data = {
            "email": member.email,
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 200
        assert request.data["user"]["email"] in member.email

    def test_wrong_email_login(self, client, db):

        data = {
            "email": fake.email(),
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 404

    def test_wrong_password_login(self, client, db):

        data = {
            "password": fake.word()
        }

        request = client.post(self.url, data)

        assert request.status_code == 400


class TestLogout:

    url = reverse("v1:users:rest_logout")

    def test_logout(self, member_auth_client):

        request = member_auth_client.post(self.url)

        assert request.status_code == 200
