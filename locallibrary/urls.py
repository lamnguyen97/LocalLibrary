from django.urls import path,include
from . import views

urlpatterns = [
 path('',views.index, name = 'index'),
 path('books',views.BookListView.as_view(), name ='book_list'),
 path('books/<int:pk>',views.BookDetailView.as_view(), name = 'book_detail'),
 path('mybooks/',views.BookBorrowListView.as_view(), name = 'book_borrow'),
 path('authors',views.AuthorListView.as_view(), name='author_list'),
 path('authors/<int:pk>',views.AuthorDetailView.as_view(), name='author_detail'),
 path('borrowed/', views.AllBorrowedListView.as_view(), name = 'borrowed')
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]


urlpatterns += [
    path('books/create/', views.BookCreate.as_view(), name='book_create')
]