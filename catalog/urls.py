from django.urls import path

from catalog import views
from catalog.views import BookListView, BookDetailView, LoanedBooksByUserListView, renew_book_librarian, AuthorCreate, \
    AuthorUpdate, AuthorDelete

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>', BookDetailView.as_view(), name = 'book-detail' ),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew', renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', AuthorUpdate.as_view(), name= 'author-update'),
    path('author/<int:pk>/delete', AuthorDelete.as_view(), name= 'author-delete'),
]


