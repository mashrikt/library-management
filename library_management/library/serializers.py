from rest_framework.serializers import ModelSerializer, SerializerMethodField

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


class BorrowCSVSerializer(ModelSerializer):
    book = SerializerMethodField()
    email = SerializerMethodField()
    user_name = SerializerMethodField()
    created_at = SerializerMethodField()
    updated_at = SerializerMethodField()

    class Meta:
        model = Borrow
        fields = ('id', 'book', 'user_name', 'email', 'status', 'note', 'created_at', 'updated_at')

    def get_book(self, obj):
        return obj.book.name

    def get_email(self, obj):
        return obj.user.email

    def get_user_name(self, obj):
        return obj.user.get_full_name()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
