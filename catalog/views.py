import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Book, BookInstance, Author
from django.contrib.auth.decorators import login_required, permission_required

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
        'number': '4'
    }

    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # TODO Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    template_name = 'author_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    success_url = reverse_lazy('index')

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # not recommended (potencial security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


