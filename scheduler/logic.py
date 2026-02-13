from datetime import date, timedelta
from .models import Module, Teacher, Classroom, ScheduleSlot


def generate_schedule():
    """
    A simple MVP algorithm to assign modules to slots.
    """
    print("--- Starting Auto-Scheduler ---")

    # 1. Get everything from the database
    modules = Module.objects.all()
    teachers = Teacher.objects.all()
    classrooms = Classroom.objects.all()

    if not teachers.exists() or not classrooms.exists():
        print(
            "Error: Please add at least one Teacher and one Classroom in the Admin panel first."
        )
        return

    # 2. Define a start date for the term (e.g., next Monday)
    current_date = date.today()

    # 3. Loop through modules and assign them one by one
    for module in modules:
        # Check if this module is already scheduled
        if ScheduleSlot.objects.filter(module=module).exists():
            print(f"Skipping {module.name} (Already scheduled)")
            continue

        # Simplified Logic: Just pick the first teacher and first room available
        # In the future, we will add "Availability" checks here.
        assigned_teacher = teachers.first()
        assigned_room = classrooms.first()

        # Calculate end date (start date + duration)
        # Assuming 1 week = 7 days
        end_date = current_date + timedelta(weeks=module.duration_weeks)

        # Create the booking in the database
        ScheduleSlot.objects.create(
            module=module,
            teacher=assigned_teacher,
            classroom=assigned_room,
            start_date=current_date,
            end_date=end_date,
        )

        print(f"Scheduled: {module.name} | {assigned_teacher} | {assigned_room}")

        # Move the start date for the next module so they don't overlap (Sequential scheduling)
        current_date = end_date

    print("--- Scheduling Complete ---")
