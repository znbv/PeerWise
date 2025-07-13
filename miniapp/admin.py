from django.contrib import admin
from .models import Tutor, StudentRequest, Feedback

# Register your models here.
admin.site.register(Tutor)
admin.site.register(StudentRequest)
admin.site.register(Feedback)
