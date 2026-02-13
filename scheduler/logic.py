from datetime import date, timedelta
from .models import Module, Teacher, Classroom, ScheduleSlot


def generate_schedule():
    """
    A smart MVP algorithm that respects teacher availability.
    """
    print("--- Starting Auto-Scheduler ---")

    # 1. Get everything from the database
    modules = Module.objects.all()
    classrooms = Classroom.objects.all()

    # We check if ANY teachers exist, but we don't load them all into a list yet
    if not Teacher.objects.exists() or not classrooms.exists():
        print(
            "Error: Please add at least one Teacher and one Classroom in the Admin panel first."
        )
        return

    # 2. Define a start date for the term (e.g., today)
    current_date = date.today()

    # 3. Loop through modules and assign them one by one
    for module in modules:
        # Check if this module is already scheduled
        if ScheduleSlot.objects.filter(module=module).exists():
            print(f"Skipping {module.name} (Already scheduled)")
            continue

        # --- LOGIC: Calculate Dates ---
        # Calculate when this module ends (Start Date + Duration)
        # We assume 1 week = 7 days
        duration_days = module.duration_weeks * 7
        proposed_end_date = current_date + timedelta(days=duration_days)

        # --- LOGIC: Find a Valid Teacher ---
        # We look for a teacher whose availability "covers" the module dates.
        # Rule:
        #   1. Teacher Start Date must be BEFORE or ON the module start date (__lte)
        #   2. Teacher End Date must be AFTER or ON the module end date (__gte)

        valid_teacher = Teacher.objects.filter(
            availability_start__lte=current_date,
            availability_end__gte=proposed_end_date,
        ).first()

        if not valid_teacher:
            print(f"❌ CONFLICT: No teacher available for {module.name}")
            print(f"   (Needs dates: {current_date} to {proposed_end_date})")
            # We skip this module and try the next one, but we don't move the current_date
            # because this slot is technically still "empty"
            continue

        # --- LOGIC: Assign Room & Save ---
        # For now, we still just grab the first room (we can upgrade this later)
        assigned_room = classrooms.first()

        ScheduleSlot.objects.create(
            module=module,
            teacher=valid_teacher,
            classroom=assigned_room,
            start_date=current_date,
            end_date=proposed_end_date,
        )

        print(f"✅ Scheduled: {module.name} | {valid_teacher.name}")
        print(f"   Dates: {current_date} to {proposed_end_date}")

        # Move the start date for the next module so they don't overlap
        current_date = proposed_end_date

    print("--- Scheduling Complete ---")
