from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

# Role-check functions based on Django groups
def is_student(user):
    return user.groups.filter(name='Student').exists()

def is_tutor(user):
    return user.groups.filter(name='Tutor').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def student_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not is_student(request.user):
                return HttpResponse("403 Forbidden: You are not a student and cannot access this page.")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def tutor_access_only(redirect_to="tutors"):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not is_tutor(request.user):
                return redirect(redirect_to)
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_access_only(redirect_to="login"):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not is_admin(request.user):    
                return redirect(redirect_to)
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

