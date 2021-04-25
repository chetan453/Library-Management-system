from django.urls import path
from . import views

urlpatterns=[
    
    path('',views.entryPage,name='entry'),
    path('login/as_user/',views.as_user,name='as_user'),
    path('search/',views.search,name='search'),
    path('login/as_librarian/',views.as_librarian,name='as_librarian'),
    path('signup/',views.signup,name='signup'),
    path('signup_librarian',views.signup_librarian,name='signup_librarian'),
    path('library/',views.student,name='index'),
    path('librarian/',views.librarian,name='librarian'),
    path('librarian.add_book',views.add_book,name='add_book'),
    path('librarian/edit=<str:bookname>',views.edit,name='edit'),
    path('librarian/delete=<str:bookname>',views.delete,name='delete'),
    path('logout/',views.logoutUser,name='logout'),
    path('borrow/<int:pk>/',views.borrow,name='borrow'),
    path('library/user_profile=<str:username>/',views.profile,name="profile"),
    path('librarian/updatestatus=<str:pk>/',views.updatestatus,name='updatestatus'),
    path('details/<int:pk>/',views.details,name='details'),
]