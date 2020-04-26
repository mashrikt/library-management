from rest_framework.serializers import ModelSerializer

from .models import Author, Book, Borrow
from ..users.relations import PresentablePrimaryKeyRelatedField
from ..users.serializers import UserDetailsSerializer


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name',)


class AuthorDetailSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name', 'dob', 'description')


class BookSerializer(ModelSerializer):
    author = PresentablePrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        presentation_serializer=AuthorSerializer,
        many=True,
    )

    class Meta:
        model = Book
        fields = ('id', 'name', 'author')


class BookDetailSerializer(ModelSerializer):
    author = PresentablePrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        presentation_serializer=AuthorDetailSerializer,
        many=True,
    )

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'description', 'count')


class BorrowSerializer(ModelSerializer):
    book = BookSerializer()
    user = UserDetailsSerializer()

    class Meta:
        model = Borrow
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'book', 'user')
