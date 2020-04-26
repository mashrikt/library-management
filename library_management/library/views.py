import csv

from django.views.generic import View
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, Borrow
from .permissions import IsAdminOrReadOnly, IsAdmin
from .serializers import (AuthorSerializer, AuthorDetailSerializer, BookSerializer, BorrowSerializer,
                          BookDetailSerializer, BorrowCSVSerializer)


class AuthorCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']


class AuthorUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'author__name']
    filterset_fields = ['count']


class BookUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookBorrowView(APIView):
    permission_classes = [IsAuthenticated]

    def get_book(self):
        book_id = self.kwargs['book_id']
        return get_object_or_404(Book, id=book_id)

    def post(self, request, *args, **kwargs):
        user = request.user
        book = self.get_book()
        borrow = Borrow.objects.create(
            user=user,
            book=book,
            created_by=user
        )
        data = {
            "id": borrow.id
        }
        return Response(data, status=status.HTTP_201_CREATED)


class BorrowListView(ListCreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['user', 'status', 'book']
    search_fields = ['book__name', 'book__author__name', 'user__name']


class BorrowUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BorrowCSVExportView(View):
    serializer_class = BorrowCSVSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="borrow.csv"'

        serializer = self.get_serializer(
            Borrow.objects.all(),
        )
        header = BorrowCSVSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            print("\n\n")
            print(row)
            print("\n\n")
            writer.writerow(row)

        return response
