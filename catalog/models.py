from django.db import models
from django.db.models.base import Model
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=100)
    isbn = models.TextField('ISBN',max_length=50, unique=True)
    genre = models.ManyToManyField(Genre,help_text='select a genre for this book')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m' , 'Maintenance'),
        ('o' , 'On loan'),
        ('a' , 'Available'),
        ('r' , 'Reserver'),
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,
    blank=True,default='m', help_text='book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id}({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},({self.first_name})'