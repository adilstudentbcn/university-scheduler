import pandas as pd
import re
from .models import CourseHistory


def parse_and_save_excel(file_obj):
    """
    Reads an uploaded Excel file and saves rows to the CourseHistory model.
    """
    try:
        # Load the file directly from memory (Django handles this)
        # sheet_name=None means "read all tabs"
        all_sheets = pd.read_excel(file_obj, sheet_name=None)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return False

    # Optional: Clear old history so we don't get duplicates every time we upload
    # If you want to keep adding to the history, delete this line.
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
            # .get() is safer than row['Code'] because it handles missing columns
            code = str(row.get("Code", "")).strip()
            name = str(row.get("Name", "")).strip()
            teacher = str(row.get("Teacher", "")).strip()

            # Skip empty rows or rows where code is 'nan'
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
