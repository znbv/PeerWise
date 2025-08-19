from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Tutor, StudentRequest, Feedback
from .forms import TutorUpdateForm, StudentRequestForm, StudentFeedbackForm, LoginForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import admin_access_only, tutor_access_only, student_access_only


class CustomloginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse_lazy('tutorlistadmin')
        elif user.groups.filter(name='Tutor').exists():
            return reverse_lazy('tutordashboard')
        elif user.groups.filter(name='Student').exists():
            return reverse_lazy('tutors')
        else:
            return reverse_lazy('tutors')


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


class StudentRequestCreateView(LoginRequiredMixin, CreateView):
    model = StudentRequest
    form_class = StudentRequestForm
    template_name = "request_form.html"
    success_url = reverse_lazy("thankyou")

    def get_initial(self):
        return {"tutor": self.kwargs.get("pk")}

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.student_name = self.request.user.username
        return super().form_valid(form)


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = StudentFeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("tutors")

    def get_initial(self):
        tutor_id = self.kwargs.get("pk")
        return {"tutor": tutor_id}


@method_decorator(admin_access_only(), name='dispatch')
class TutorViewForAdmin(LoginRequiredMixin, ListView):
    model = Tutor
    template_name = 'admin_dashboard.html'
    context_object_name = 'tutorlistadmin'


@login_required
@admin_access_only()
def update_delete_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    form = TutorUpdateForm(request.POST or None, instance=tutor)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "Update" and form.is_valid():
            form.save()
            messages.success(request, "Tutor information updated successfully!")
            return redirect("tutorlistadmin")

        elif action == "Delete":
            tutor.delete()
            messages.success(request, "Tutor deleted successfully!")
            return redirect("tutorlistadmin")

    return render(request, "admin_dashboard.html", {
        "form": form,
        "tutorlistadmin": Tutor.objects.all(),
    })


def thankyou(request):
    return render(request, "thank_you.html")


@login_required
@admin_access_only()
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  

@login_required
@student_access_only()
def student_dashboard(request):
    requests = StudentRequest.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'stud_req': requests})


@tutor_access_only(redirect_to='tutors') 
@login_required
def tutor_requests_view(request):
    try:
        tutor = Tutor.objects.get(user=request.user)
        requests = StudentRequest.objects.filter(tutor=tutor)
    except Tutor.DoesNotExist:
        requests = []
    return render(request, 'tutor_dashboard.html', {'requests': requests})


@login_required
def handle_request_action(request, request_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        student_request = get_object_or_404(StudentRequest, id=request_id)

        if student_request.tutor.user == request.user:
            if action == 'accept':
                student_request.status = 'ACCEPTED'
            elif action == 'reject':
                student_request.status = 'REJECTED'
            student_request.save()

    return redirect('tutordashboard')
