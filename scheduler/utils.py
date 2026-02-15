import pandas as pd
import re
from datetime import date
from .models import CourseHistory, Teacher, Course, Term


def parse_and_save_excel(file_obj):
    """
    Reads an uploaded Excel file and saves rows to the CourseHistory model.
    """
    try:
        # Load the file directly from memory (Django handles this)
        all_sheets = pd.read_excel(file_obj, sheet_name=None)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return False

    # Optional: Clear old history so we don't get duplicates every time we upload
    CourseHistory.objects.all().delete()

    print(f"📂 Found tabs: {list(all_sheets.keys())}")

    saved_count = 0

    for tab_name, df in all_sheets.items():
        # Extract Year from Tab Name (e.g. "2024-2025" -> 2024)
        match = re.search(r"(\d{4})", str(tab_name))
        if match:
            current_year = int(match.group(1))
        else:
            continue  # Skip tabs without years

        # Iterate through rows in this specific tab
        for index, row in df.iterrows():
            code = str(row.get("Code", "")).strip()
            name = str(row.get("Name", "")).strip()
            teacher = str(row.get("Teacher", "")).strip()

            # Skip empty rows or 'nan'
            if not code or code.lower() == "nan":
                continue

            # Save to Database
            CourseHistory.objects.create(
                course_code=code,
                course_name=name,
                year=current_year,
                teacher_name=teacher,
            )
            saved_count += 1

    print(f"✅ Successfully saved {saved_count} history records.")
    return True


def populate_db_from_history():
    """
    The 'Bridge' Function:
    Taking data from CourseHistory and filling the real Teacher/Course tables.
    """

    # 1. Get all history
    history_entries = CourseHistory.objects.all()

    if not history_entries.exists():
        return 0, 0  # Nothing to import

    # 2. Logic to find the "Most Recent" version of every course
    # Dictionary: { 'MATH101': <CourseHistory Object> }
    unique_courses = {}

    for entry in history_entries:
        code = entry.course_code

        # If we haven't seen this code, OR this entry is newer than what we have stored
        if code not in unique_courses:
            unique_courses[code] = entry
        else:
            if entry.year > unique_courses[code].year:
                unique_courses[code] = entry

    # 3. Create a Default Term (Required for Courses)
    # We need a place to put these courses. We'll create a generic term.
    default_term, created = Term.objects.get_or_create(
        name="Imported Term",
        defaults={"start_date": date(2025, 1, 1), "end_date": date(2025, 3, 30)},
    )

    created_teachers = 0
    created_courses = 0

    # 4. Loop through the "Winners" and create real database objects
    for code, entry in unique_courses.items():

        # --- Step A: Handle Teacher ---
        teacher_obj = None
        if entry.teacher_name and entry.teacher_name.lower() != "nan":
            # get_or_create checks if name exists. If yes, it returns it. If no, creates it.
            teacher_obj, t_created = Teacher.objects.get_or_create(
                name=entry.teacher_name
            )
            if t_created:
                created_teachers += 1

        # --- Step B: Handle Course ---
        # We use 'update_or_create' so if we run this twice, it doesn't duplicate courses
        course_obj, c_created = Course.objects.update_or_create(
            name=entry.course_name,  # Identifying the course by Name
            defaults={
                "term": default_term,
                "teacher": teacher_obj,
                "preferred_time": "MORNING",  # Default
            },
        )
        if c_created:
            created_courses += 1

    print(
        f"🎉 Import Complete: Created {created_teachers} Teachers and {created_courses} Courses."
    )
    return created_teachers, created_courses
