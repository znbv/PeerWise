from django.urls import path
from . import views
urlpatterns = [
    path( "", views.TutorListView.as_view(), name="tutors"),  # tutors is the name of the URL pattern, which can be used in templates to link to this view
    path("request/<int:pk>/", views.StudentRequestCreateView.as_view(),name="student_request"),
    path("feedback/<int:pk>/", views.FeedbackCreateView.as_view(), name="leave_feedback"),
    path("thankyou/", views.thankyou, name="thankyou"),  # URL for the thank you page
    path("adminaccess/", views.TutorViewForAdmin.as_view(), name="tutorlistadmin"),
    path("adminaccess/<int:pk>/update", views.update_delete_tutor, name="update_delete_tutor"),
]
