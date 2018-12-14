from django.shortcuts import render
from django.views import generic
from .models import Book,BookInstance,Author,Genre

def index(request):
    template_name = 'index.html'
    num_book = Book.objects.count()
    num_copy = BookInstance.objects.count()
    num_author = Author.objects.count()
    num_avail = BookInstance.objects.filter(status='a').count()
    num_genre = Genre.objects.count()
    return render(request,'index.html', {'num_book':num_book,'num_copy':num_copy,'num_author':num_author,'num_avail':num_avail,
                                         'num_genre': num_genre})
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