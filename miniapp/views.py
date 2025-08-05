from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Tutor, StudentRequest, Feedback
from .forms import TutorUpdateForm, StudentRequestForm, StudentFeedbackForm, LoginForm
from django.contrib import messages

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin   # Ensures that the user is logged in to access certain views
from django.contrib.auth.decorators import login_required  # Decorator to ensure the user is logged in
from .decorators import restrict_access_to_groups  # Custom decorators for access control   
# Create your views here.

class CustomloginView(LoginView):
    template_name = "login.html"  # Use login.html to render the login page
    form_class = LoginForm
    fields = "__all__"
    redirect_authenticated_user = True  # Redirects authenticated users to the homepage

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse_lazy('tutorlistadmin')
        elif user.groups.filter(name='Tutor').exists():
            return reverse_lazy('tutordashboard')
        elif user.groups.filter(name='Student').exists():
            return reverse_lazy('tutors')  # Redirects to the tutors list for students
        else:
            return reverse_lazy('tutors')  # fallback
       

def thankyou(request):
    return render(request, "thank_you.html") # simply diplays the thankyou page.

class TutorListView(ListView):
    model = Tutor # display the list of tutors from the model Tutor
    template_name = "homepage.html" # use homepage.html to show the view in browser
    context_object_name = "tutors" # use tutors to access objects from Tutor model
    
    # Gets all tutors, check if the user typed any input if yes, only display the filtered result or else display all tutors in database.
    def get_queryset(self):
        queryset = super().get_queryset() # gets all tutors from the db, similar to Tutor.objects.all()
        subject = self.request.GET.get("q") # checks for user input in the url or in the search bar
        if subject:
            queryset = queryset.filter(subject__icontains=subject) # performs a case insensitive search 
        return queryset # return either all tutors or filtered

    # Add feedback to each tutor
    def get_context_data(self, **kwargs): # to add extra data to be used in the HTML templates
        context = super().get_context_data(**kwargs)
        feedbacks = Feedback.objects.all() # get all feedback entries from the db
        tutors = context["tutors"] # set earlier
        for tutor in tutors:
            tutor.feedback_list = feedbacks.filter(tutor_id=tutor.id) # creates a new attr feedback_list
        return context

class StudentRequestCreateView(LoginRequiredMixin, CreateView):
    model = StudentRequest
    form_class = StudentRequestForm
    template_name = "request_form.html"
    success_url = reverse_lazy("thankyou")

    # Pre-fill the tutor field if the URL carries  /request/<pk>/
    def get_initial(self):
        return {"tutor": self.kwargs.get("pk")}

    # Automatically attach the logged-in student’s info before saving
    def form_valid(self, form):
        req = form.save(commit=False)                 # don’t hit the DB yet
        req.student_name = self.request.user.username # set student name
        # req.contact_email = self.request.user.email   # optional: set email
        req.save()                                    # now save once
        return super().form_valid(form)               # let the mixin handle redirect


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = StudentFeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("tutors")  # Redirects to homepage after submission

    def get_initial(self):
        tutor_id = self.kwargs.get("pk" )  
        return {"tutor": tutor_id} 

class TutorViewForAdmin(LoginRequiredMixin, ListView):
    model = Tutor
    template_name = 'admin_dashboard.html'
    context_object_name= 'tutorlistadmin' # Tutors is the name of the variable that will be used in the template to access the list of tutors

# Handle both update and delete in one view
@login_required  
def update_delete_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    form = TutorUpdateForm(request.POST or None, instance=tutor)  # Create a form pre-filled with tutor data; use POST data if submitted, else empty form

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "Update" and form.is_valid():
            form.save()
            messages.success(request, "Tutor information updated successfully!" )
            return redirect("tutorlistadmin")

        elif action == "Delete":
            tutor.delete()
            messages.success(request, "Tutor deleted successfully!")
            return redirect("tutorlistadmin")

    return render(request,"admin_dashboard.html", {"form": form, "tutorlistadmin": Tutor.objects.all()},)

@restrict_access_to_groups(['Admin'])
def admin_dashboard(request):
    return render(request, 'tutorlistadmin')

@restrict_access_to_groups(['Student'])
def student_dashboard(request):
     return render(request, 'tutors')

@restrict_access_to_groups(['Tutor'])
def tutor_dashboard(request):
     return render(request, 'tutor_dashboard.html')

def student_view(request):
     return render(request, 'student_dashboard.html')

@login_required
def tutor_requests_view(request):
    user = request.user

    try:
        tutor = Tutor.objects.get(user=request.user) 
        requests = StudentRequest.objects.filter(tutor=tutor)
    
    except Tutor.DoesNotExist:
        requests = []
        
    return render(request, 'tutor_dashboard.html', {'requests': requests})

# def tutor_requests_view(request):
#     user = request.user
#     print("Logged-in user:", user)

#     try:
#         tutor = Tutor.objects.get(user=user)
#         print("Tutor object:", tutor)
        
#         requests = StudentRequest.objects.filter(tutor=tutor)
#         print("Requests count:", requests.count())

#     except Tutor.DoesNotExist:
#         print("No Tutor object linked to this user.")
#         requests = []

#     return render(request, 'tutor_dashboard.html', {'requests': requests})

@login_required
def handle_request_action(request, request_id):
    if request.method == 'POST':
        action = request.POST.get('action')  # 'accept' or 'reject'
        student_request = get_object_or_404(StudentRequest, id=request_id)

        if student_request.tutor.user == request.user:  # make sure this request belongs to logged-in tutor
            if action == 'accept':
                student_request.accepted = True
            elif action == 'reject':
                student_request.accepted = False
            student_request.save()

    return redirect('tutordashboard')  # redirect back to dashboard
