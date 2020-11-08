from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from catalog.models import Book, BookInstance, Author


def test_view(request):
    return HttpResponse('Homepage')


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'




