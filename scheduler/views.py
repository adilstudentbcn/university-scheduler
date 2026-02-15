from django.shortcuts import render, redirect
from django.contrib import messages  # <--- THIS WAS THE MISSING LINE
from .models import ScheduleSlot, CourseHistory
from .logic import generate_schedule
from .utils import parse_and_save_excel, populate_db_from_history


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
        generate_schedule()  # This runs your scheduling logic!
    return redirect("schedule_list")


def upload_history_view(request):
    """
    Handles the Excel file upload and triggers the parser.
    """
    if request.method == "POST" and request.FILES.get("excel_file"):
        myfile = request.FILES["excel_file"]
        # Pass the file directly to our parser
        success = parse_and_save_excel(myfile)
        if success:
            return redirect("history_list")
    return render(request, "scheduler/upload_history.html")


def history_list_view(request):
    """
    Show the table of parsed data, sorted by Year (newest first).
    """
    history = CourseHistory.objects.all().order_by("-year", "course_name")
    return render(request, "scheduler/history_list.html", {"history": history})


def populate_db_view(request):
    if request.method == "POST":
        # Check if history actually exists first
        if not CourseHistory.objects.exists():
            messages.warning(
                request, "⚠️ No history found! Please upload an Excel file first."
            )
            # CHANGE: Redirect back to the same page (View History)
            return redirect("history_list")

        t_count, c_count = populate_db_from_history()
        messages.success(
            request,
            f"✅ Import Successful! Created {t_count} Teachers and {c_count} Courses.",
        )
        # Keep this one going to the schedule_list so you can see the results
        return redirect("schedule_list")

    return redirect("history_list")
