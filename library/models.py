from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
# Create your models here.

class Book(models.Model):
    book_title=models.CharField(max_length=100)
    author=models.CharField(max_length=250)
    publisher=models.CharField(max_length=1000)
    summary=models.CharField(max_length=90000)
    Isbn=models.CharField(max_length=20)
    location=models.CharField(max_length=10)
    count=models.IntegerField(default=1)

    def __str__(self):
        return self.book_title + '-' +self.author


class Borrowed(models.Model):
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    id = models.CharField(primary_key=True,default=uuid.uuid4,max_length=3000)
    borrowed_number = models.IntegerField(default=0)
    STATUS_CHOICES = [
        ('1','PENDING'),
        ('2','APPROVE'),
        ('3','REJECT'),
    ]

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='1')

    issue_date = models.DateTimeField(null=True,blank=True)
    due_date = models.DateTimeField(null = True, blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.book.book_title
