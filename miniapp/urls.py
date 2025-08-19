from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
# Defines the URL routes for the Django app. Tells Django which view to use when user visits a specific address on website. 

urlpatterns = [
    path("login/", views.CustomloginView.as_view(), name="login"),  # Custom login view
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),  # Logout view, redirects to login page after logout
    path( "", views.TutorListView.as_view(), name="tutors"),  # tutors is the name of the URL pattern, which can be used in templates to link to this view
    path("request/<int:pk>/", views.StudentRequestCreateView.as_view(),name="student_request"), # send request to a particular tutor
    path("feedback/<int:pk>/", views.FeedbackCreateView.as_view(), name="leave_feedback"), # leave feedback for a particular tutor
    path("thankyou/", views.thankyou, name="thankyou"),  # URL for the thank you page
    path("adminaccess/", views.TutorViewForAdmin.as_view(), name="tutorlistadmin"),
    path("adminaccess/<int:pk>/", views.update_delete_tutor, name="update_delete_tutor"), # update or delete a particular tutor
    path("tutor_dashboard/", views.tutor_requests_view, name="tutordashboard"),  # Tutor dashboard for logged-in tutors
    path('handle_request_action/<int:request_id>/', views.handle_request_action, name='handle_request_action'),
    path("student_dashboard/", views.student_dashboard, name="studentdashboard"),  # Student dashboard for logged-in students
     
]
