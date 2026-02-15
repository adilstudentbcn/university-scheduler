from .models import Course, ScheduleSlot, Classroom


def generate_schedule():
    print("--- Starting Parallel Auto-Scheduler ---")

    # Clear old schedule
    ScheduleSlot.objects.all().delete()

    courses = Course.objects.all()
    classrooms = Classroom.objects.all()

    for course in courses:
        # 1. Get the dates from the Term assigned to this course
        term_start = course.term.start_date
        term_end = course.term.end_date

        # 2. Find a room that is NOT occupied at this specific time slot
        # We look for conflicts in the SAME term and SAME time slot
        occupied_rooms = ScheduleSlot.objects.filter(
            term=course.term, time_slot=course.preferred_time
        ).values_list("classroom", flat=True)

        available_room = classrooms.exclude(id__in=occupied_rooms).first()

        if not available_room:
            print(f"❌ CONFLICT: No room for {course.name} at {course.preferred_time}")
            continue

        # 3. Create the slot
        # Note: If course has a manually assigned teacher, use them.
        assigned_teacher = course.teacher
        if not assigned_teacher:
            print(f"⚠️ Warning: {course.name} has no teacher assigned.")
            # logic could auto-assign a teacher here if you wanted
            continue

        ScheduleSlot.objects.create(
            course=course,
            teacher=assigned_teacher,
            classroom=available_room,
            term=course.term,
            start_date=term_start,
            end_date=term_end,
            time_slot=course.preferred_time,
        )
        print(
            f"✅ Scheduled: {course.name} ({course.preferred_time}) in {available_room}"
        )

    print("--- Scheduling Complete ---")
