import pytest
import factory
from django.urls import reverse

from .factories import AuthorFactory, BookFactory
from ..models import Author, Book, Borrow


class TestAuthor:
    url = reverse("v1:authors:create")

    @pytest.fixture
    def data(self):
        return factory.build(dict, FACTORY_CLASS=AuthorFactory)

    def test_created_by_admin(self, admin_auth_client, data, db):
        request = admin_auth_client.post(self.url, data)
        assert request.status_code == 201
        assert Author.objects.filter(id=request.json()['id']).exists()

    def test_member_cant_create(self, member_auth_client, data, db):
        request = member_auth_client.post(self.url, data)
        assert request.status_code == 403
        assert not Author.objects.filter(name=data['name']).exists()


class TestBook:
    url = reverse("v1:books:create")

    @pytest.fixture
    def author(self):
        return AuthorFactory()

    @pytest.fixture
    def data(self, author):
        data = factory.build(dict, FACTORY_CLASS=BookFactory)
        data['author'] = [author.id]
        return data

    @pytest.fixture
    def book(self, db):
        return BookFactory()

    def test_created_by_admin(self, admin_auth_client, data, db):
        request = admin_auth_client.post(self.url, data)
        assert request.status_code == 201
        assert Book.objects.filter(id=request.json()['id']).exists()

    def test_member_cant_create(self, member_auth_client, data, db):
        request = member_auth_client.post(self.url, data)
        assert request.status_code == 403
        assert not Book.objects.filter(name=data['name']).exists()

    def test_book_borrow(self, member_auth_client, book, db):
        url = reverse("v1:books:borrow", kwargs={'book_id': book.id})
        request = member_auth_client.post(url, {})
        assert request.status_code == 201
        borrow_id = request.json()['id']
        assert Borrow.objects.get(id=borrow_id)

    def test_cant_book_borrow_when_not_logged_in(self, client, book, db):
        url = reverse("v1:books:borrow", kwargs={'book_id': book.id})
        request = client.post(url, {})
        assert request.status_code == 401


class TestBorrow:

    url = reverse("v1:borrow:list")

    @pytest.fixture
    def borrow(self):
        return AuthorFactory()

    def test_admin_can_access(self, admin_auth_client, borrow, db):
        request = admin_auth_client.get(self.url)
        assert request.status_code == 200

    def test_member_can_not_access(self, member_auth_client, borrow, db):
        request = member_auth_client.get(self.url)
        assert request.status_code == 403