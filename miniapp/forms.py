from django import forms
from .models import Tutor, StudentRequest, Feedback


class TutorUpdateForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ["name", "subject", "description", "contact_email"]


class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ["tutor", "student_name", "message", "contact_email"]
        widgets = {
            "tutor": forms.Select(attrs={"class": "form-control"}),
            "student_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your name"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your request here...",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your email"}
            ),
        }

class StudentFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["tutor", "student_name", "rating", "comment"]
        widgets={
            "tutor":forms.Select(attrs={"class":"form-control"}), 
            "student_name":forms.TextInput(attrs={"class":"form-control", "placeholder": "Your name"}), 
            "rating":forms.NumberInput(attrs={"class":"form-control", "placeholder": "Rate your tutor out of 5"}),
            "comment":forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment:"}) 
        }
