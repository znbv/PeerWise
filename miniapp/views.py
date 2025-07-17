from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Tutor, StudentRequest, Feedback
from .forms import TutorUpdateForm, StudentRequestForm, StudentFeedbackForm
# Create your views here.

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


class StudentRequestCreateView(CreateView): #allow students to req for a tutor using a form
    model = StudentRequest # Model used to save new student requests
    form_class = StudentRequestForm
    template_name = 'request_form.html'
    success_url = reverse_lazy('thankyou') # Redirect to the thank you page after successful request. 

    def get_initial(self): # prefills the tutor field if a specifc tutor ID was in the url
        tutor_id = self.kwargs.get('pk') # 1-M relationship allowed each request to be linked to a specific tutor
        return {"tutor": tutor_id }  # pr-fill the tutor field in the form with this tutor_id

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = StudentFeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("tutors")  # Redirects to homepage after submission

    def get_initial(self):
        tutor_id = self.kwargs.get("pk" )  
        return {"tutor": tutor_id} 

class TutorViewForAdmin(ListView):
    model = Tutor
    template_name = 'admin_dashboard.html'
    context_object_name= 'tutorlistadmin' # Tutors is the name of the variable that will be used in the template to access the list of tutors

# Handle both update and delete in one view
def update_delete_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    form = TutorUpdateForm(request.POST or None, instance=tutor)  # Create a form pre-filled with tutor data; use POST data if submitted, else empty form

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "Update" and form.is_valid():
            form.save()
            return redirect("tutors")

        elif action == "Delete":
            tutor.delete()
            return redirect("tutors")

    return render(request, "admin_dashboard.html", {"form": form, "tutors": Tutor.objects.all()})
