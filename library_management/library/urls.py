from django.urls import path, include

from .views import AuthorCreateView, AuthorUpdateView, BookCreateView, BookUpdateView, BorrowListView, BorrowUpdateView, \
    BookBorrowView, BorrowCSVExportView

author_urlpatterns = [
    path('', AuthorCreateView.as_view(), name='create'),
    path('<int:pk>/', AuthorUpdateView.as_view(), name='update'),

]

book_urlpatterns = [
    path('', BookCreateView.as_view(), name='create'),
    path('<int:pk>/', BookUpdateView.as_view(), name='update'),
    path('<int:book_id>/borrow/', BookBorrowView.as_view(), name='borrow'),

]

borrow_urlpatterns = [
    path('', BorrowListView.as_view(), name='list'),
    path('<int:pk>/', BorrowUpdateView.as_view(), name='update-update'),
    path('csv/', BorrowCSVExportView.as_view(), name='csv'),

]
