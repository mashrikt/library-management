import factory
from django.contrib.auth import get_user_model
from faker import Faker

from ..models import Author, Book, Borrow
from ...users.tests.factories import UserFactory

fake = Faker()
User = get_user_model()


class AuthorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Author

    name = factory.Faker("name")


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    name = factory.Faker("name")

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups were passed in, use them
            for author in extracted:
                self.author.add(author)
        else:
            author = AuthorFactory()
            self.author.add(author)


class BorrowFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Borrow

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)
