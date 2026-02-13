from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import ScheduleSlot


def schedule_list(request):
    # 1. Fetch all slots from the database
    slots = ScheduleSlot.objects.all().order_by("start_date")

    # 2. Send them to the HTML template
    return render(request, "scheduler/schedule_list.html", {"slots": slots})
