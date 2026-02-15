from django.shortcuts import render, redirect
from .models import ScheduleSlot
from .logic import generate_schedule  # Import your automation script


def schedule_list(request):
    """
    1. Fetch all slots from the database.
    2. Send them to the HTML template to be displayed.
    """
    slots = ScheduleSlot.objects.all().order_by("start_date")
    return render(request, "scheduler/schedule_list.html", {"slots": slots})


def run_scheduler(request):
    """
    Trigger the auto-scheduler when the button is clicked,
    then go back to the list.
    """
    if request.method == "POST":
        generate_schedule()  # <--- This runs your logic!

    return redirect("schedule_list")
