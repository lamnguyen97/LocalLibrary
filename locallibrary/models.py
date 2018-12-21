from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
import uuid


class Genre(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=True,blank=True)
    dod = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)

    def get_absolute_url(self):
        return reverse('author_detail',args=[self.id])


class Book(models.Model):
    title = models.CharField(max_length=500)
    summary = models.CharField(max_length=1000)
    imprint = models.CharField(max_length=500)
    ISBN = models.CharField('ISBN',max_length = 13)
    author = models.ForeignKey(Author, on_delete = models.SET_NULL,null=True)
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail',args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4())
    due_back = models.DateField()
    book = models.ForeignKey(Book,on_delete = models.SET_NULL,null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS =(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved')
    )
    status = models.CharField(max_length=1,choices=LOAN_STATUS,default='m',help_text='Status of the book')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("CanViewBorrowed","View Books Borrowed"),)

    def __str__(self):
        return '{} ({})'.format(self.uid,self.book.title)




# Create your models here.
