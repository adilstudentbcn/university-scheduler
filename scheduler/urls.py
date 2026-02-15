from django.urls import path
from . import views

urlpatterns = [
    # 1. The Main Schedule Page
    path("", views.schedule_list, name="schedule_list"),
    path("run-scheduler/", views.run_scheduler, name="run_scheduler"),
    # 2. The New History Pages
    path("upload-history/", views.upload_history_view, name="upload_history"),
    path("history/", views.history_list_view, name="history_list"),
]
