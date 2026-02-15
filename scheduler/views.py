from django.shortcuts import render, redirect
from .models import ScheduleSlot, CourseHistory  # <--- Added CourseHistory
from .logic import generate_schedule
from .utils import parse_and_save_excel  # <--- Added your new utility


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


def upload_history_view(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        myfile = request.FILES["excel_file"]

        # Pass the file directly to our parser
        success = parse_and_save_excel(myfile)

        if success:
            return redirect("history_list")

    return render(request, "scheduler/upload_history.html")


def history_list_view(request):
    # Show the table of parsed data, sorted by Year (newest first)
    history = CourseHistory.objects.all().order_by("-year", "course_name")
    return render(request, "scheduler/history_list.html", {"history": history})
