from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank = True)  # One-to-One relationship with User model
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_request = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.subject})"
    
class StudentRequest(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)  # ForeignKey to Tutor model
    student_name = models.CharField(max_length=150)
    message = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateTimeField(null=True, blank=True)  
    accepted = models.BooleanField(null=True, blank=True)  

    def __str__(self):
        return f"{self.student_name} -> {self.tutor.name}"

class Feedback(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE) # ForeignKey to Tutor model
    student_name = models.CharField(max_length=150)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True) #blank=true, means you can leave it empty in forms, null=True means it can be null in the database
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will be set to the current date and time when the object is created

    def __str__(self):
        return f"Feedback from {self.student_name} for {self.tutor.name}"
