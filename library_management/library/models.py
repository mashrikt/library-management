from django.db import models

from ..users.models import User


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dob = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    name = models.CharField(max_length=200, unique=True)
    author = models.ManyToManyField(Author)
    description = models.TextField(blank=True)
    # total number of this book available in the library
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name}"


class BorrowStatus(object):
    REQUEST = 'request'
    APPROVED = 'approved'
    RETURNED = 'returned'
    OVERDUE = 'overdue'

    CHOICES = (
        (REQUEST, 'request'),
        (APPROVED, 'approved'),
        (RETURNED, 'returned'),
        (OVERDUE, 'overdue'),
    )


class Borrow(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="created_by")
    updated_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="updated_by")
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=BorrowStatus.CHOICES, default=BorrowStatus.REQUEST)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.book} > {self.user}"
