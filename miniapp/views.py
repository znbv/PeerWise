from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Tutor, StudentRequest, Feedback
from .forms import TutorUpdateForm, StudentRequestForm, StudentFeedbackForm
# Create your views here.

def thankyou(request):
    return render(request, "thank_you.html") #simply diplays the thankyou page.

class TutorListView(ListView):
    model = Tutor
    template_name = "homepage.html"
    context_object_name = "tutors"

    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.GET.get("q")
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedbacks = Feedback.objects.all()
        tutors = context["tutors"]
        for tutor in tutors:
            tutor.feedback_list = feedbacks.filter(tutor_id=tutor.id)

        return context


class StudentRequestCreateView(CreateView): #allow students to req for a tutor using a form
    model = StudentRequest
    form_class = StudentRequestForm
    template_name = 'request_form.html'
    success_url = reverse_lazy('thankyou') # Redirect to the thank you page after successful request. 

    def get_initial(self): #prefills the tutor field if a specifc tutor ID was in the url
        tutor_id = self.kwargs.get('pk') #1-M relationship allowed each request to be linked to a specific tutor
        return {'tutor': tutor_id}

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = StudentFeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("tutors")  # Redirects to homepage after submission

    def get_initial(self):
        tutor_id = self.kwargs.get("pk" )  # 1-M relationship allowed each request to be linked to a specific tutor
        return {"tutor": tutor_id}

class TutorViewForAdmin(ListView):
    model = Tutor
    template_name = 'admin_dashboard.html'
    context_object_name= 'tutorlistadmin' #tutors is the name of the variable that will be used in the template to access the list of tutors

def update_delete_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    form = TutorUpdateForm(request.POST or None, instance=tutor)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "Update" and form.is_valid():
            form.save()
            return redirect("tutors")

        elif action == "Delete":
            tutor.delete()
            return redirect("tutors")

    return render(
        request, "admin_dashboard.html", {"form": form, "tutors": Tutor.objects.all()}
    )
