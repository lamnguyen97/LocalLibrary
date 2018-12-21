from django.shortcuts import render
from django.views import generic
from .models import Book,BookInstance,Author,Genre
from datetime import date,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from locallibrary.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    template_name = 'index.html'
    num_book = Book.objects.count()
    num_copy = BookInstance.objects.count()
    num_author = Author.objects.count()
    num_avail = BookInstance.objects.filter(status='a').count()
    num_genre = Genre.objects.count()
    num_visit = request.session.get("num_visit",0)
    request.session["num_visit"] = num_visit+1
    return render(request,'index.html', {'num_book':num_book,'num_copy':num_copy,'num_author':num_author,'num_avail':num_avail,
                                         'num_genre': num_genre,'num_visit': num_visit})
# Create your views here.
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):

    model = Book
    content_object_name ="book"
    template_name ='book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name ='author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name ='author_detail.html'

class BookBorrowListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    context_object_name  = 'book_list'
    template_name = 'book_borrow.html'

    def get_queryset(self):

        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    context_object_name = "borrowed_list"
    template_name = "all_borrowed.html"
    permission_required = 'locallibrary.CanViewBorrowed'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
