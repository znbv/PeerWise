from django import forms
from .models import Tutor, StudentRequest, Feedback


class TutorUpdateForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ["name", "subject", "description", "contact_email"]


class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ["tutor", "message", "contact_email", "preferred_date"]
        widgets = {
            "tutor": forms.Select(attrs={"class": "form-control"}),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your request here...",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your email"}
            ),
            "preferred_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                })
        }
    # # When a student makes a request, the tutor’s sent_request field is set to True and saved.
    # def save(self, commit = True):
    #     self.instance.tutor.sent_request = True
    #     tutor= self.instance.tutor
    #     tutor.save()
    #     return super().save(commit)
    
    


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

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': True,
        }),
        label="Username"
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )
