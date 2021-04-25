from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import unauthenticated_user,allowed_user
from django.contrib.auth.models import Group
from django.contrib.postgres.search import SearchVector
from .forms import BookEditForm,UpdateStatusForm
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.

def entryPage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:
    return render(request,'library/entry_page.html')


@unauthenticated_user
def signup(request):
    forms=UserCreationForm()
    if request.method=='POST':
        forms=UserCreationForm(request.POST)
        if forms.is_valid():
            user=forms.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            username=forms.cleaned_data.get("username")
            messages.success(request,'account has been created for user '+ username)
            return redirect('entry')
    return render(request,'library/signup.html',{'forms':forms,})    


# @unauthenticated_user
def signup_librarian(request):
    forms=UserCreationForm()
    if request.method=='POST':
        forms=UserCreationForm(request.POST)
        if forms.is_valid():
            user=forms.save()
            group = Group.objects.get(name='no access')
            user.groups.add(group)
            username=forms.cleaned_data.get("username")
            messages.success(request,'Your request for librarian is sent to admin. You will be able to login when admin approved your request')
            return redirect('entry')
    return render(request,'library/signup.html',{'forms':forms,})    


@unauthenticated_user
def as_user(request):
    forms=UserCreationForm()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user is not None:
            
            group = user.groups.all()[0].name
            if group=="student":
                login(request,user)
                return redirect('index')  
            else:
                messages.info(request,"You cannot login here")
        else:
            messages.info(request,"username or password incorrect")

    return render(request,'library/asuser.html',{'forms':forms,})


def logoutUser(request):
    logout(request)
    return redirect('entry')


@unauthenticated_user
def as_librarian(request):
    forms=UserCreationForm()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user is not None:
            group = user.groups.all()[0].name
            if group=="librarian":
                login(request,user)
                return redirect('librarian')  
            else:
                messages.info(request,"You cannot login here")
        else:
            messages.info(request,"username or password incorrect")    
    
    return render(request,'library/as_librarian.html',{'forms':forms,})


@allowed_user('librarian')
def librarian(request):
    books=Book.objects.order_by('-id')[:8]
    borrows=Borrowed.objects.all()[:6]
    context={
        'books':books,
        'borrows':borrows,
    }
    return render(request,'library/main.html',context)


@login_required(login_url='entry')
@allowed_user('student')
def student(request):    
    books=Book.objects.order_by('-id')[:6]
    context={
        'books':books,
    }
    return render(request,'library/index.html',context)

@login_required(login_url='entry')
def details(request,pk):
    details=Book.objects.get(id = pk)
    username=request.user
    user=User.objects.get(username=username)
    context={
        'book':details,
        'user':user,
    }
    return render(request,'library/details.html',context)

@login_required(login_url='entry')
def search(request):
    value=request.GET["search"]

    searchvalue=Book.objects.filter(book_title__icontains=value)
    context={
        'searchvalue':searchvalue,
    }
    return render(request,'library/booksearch.html',context)

@login_required(login_url='entry')
def add_book(request):
    form=BookEditForm()
    if request.method=='POST':
        form = BookEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('librarian')
    context={
        'form':form
    }
    return render(request,'library/edit_book.html',context)

@login_required(login_url='entry')
def edit(request,bookname):
    book=Book.objects.get(book_title=bookname)
    form=BookEditForm(instance=book)
    if request.method=='POST':
        form = BookEditForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('librarian')
    context={
        'form':form
    }
    return render(request,'library/edit_book.html',context)


@login_required(login_url='entry')
def delete(request,bookname):
    book=Book.objects.get(book_title=bookname)
    if request.method=='POST':
        book.delete()
        return redirect('librarian')
    context={
        'book':book
    }
    return render(request,'library/delete.html',context)


@login_required(login_url='entry')
def borrow(request,pk):
    user=request.user
    book=Book.objects.get(id = pk)
    if request.method == 'POST':
        count = Borrowed.objects.filter(borrower=user).count()
        if count < 10 :
            borrow=Borrowed(borrower=user,book=book)
            if book.count > 0 :
                book.count = book.count - 1
                book.save()
                borrow.issue_date=timezone.now()
                borrow.due_date = borrow.issue_date + timedelta(days=10)
                borrow.borrowed_number = borrow.borrowed_number + 1

            else:
                messages.info("Sorry! This book is not available in library")
        else:
            messages.info("You have exceeds your borrow limit you cannot borrow more")    
        borrow.save()

    return redirect('details',book.book_title)    


def profile(request,username):
    user = User.objects.get(username = username)
    borrows = Borrowed.objects.filter(borrower=user)
    context={
        'borrows':borrows,
        'user' :user,
    }
    return render(request,'library/profile.html',context)


def updatestatus(request,pk):
    borrow = Borrowed.objects.get(id = pk)
    form = UpdateStatusForm(instance=borrow)
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST,instance = borrow)
        if form.is_valid():
            form.save()
            return redirect('librarian')
    context={
        'form':form,
    }    
    return render(request,'library/update_status.html',context)
