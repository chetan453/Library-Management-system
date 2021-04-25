from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowed_user(allowed_role=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if str(group) in allowed_role:
                return view_func(request,*args,**kwargs)
            else:
                messages.info(request,"you cannot login here")
                return redirect('as_user')
            
        return wrapper_func
    return decorator
                

