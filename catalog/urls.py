from django.urls import path

from catalog import views
from catalog.views import BookListView, BookDetailView, LoanedBooksByUserListView

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>', BookDetailView.as_view(), name = 'book-detail' ),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed')
]

