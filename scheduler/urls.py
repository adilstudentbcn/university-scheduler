from django.urls import path
from . import views

urlpatterns = [
    # The main page with the table
    path("", views.schedule_list, name="schedule_list"),
    # The new hidden URL that runs the logic
    path("run-scheduler/", views.run_scheduler, name="run_scheduler"),
]
