from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Term(models.Model):
    """
    Represents the Time Block (e.g., 'Module 5').
    """

    name = models.CharField(max_length=50)  # e.g. "Module 05"
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class Course(models.Model):
    """
    Represents the Subject (e.g., 'Calculus 1', 'Motion Design').
    """

    TIME_CHOICES = [
        ("MORNING", "09:00 - 12:20"),
        ("AFTERNOON", "13:00 - 16:20"),
        ("EVENING", "17:00 - 20:20"),
    ]

    name = models.CharField(max_length=100)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="courses")
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    preferred_time = models.CharField(
        max_length=20, choices=TIME_CHOICES, default="MORNING"
    )
    duration_weeks = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.name} ({self.preferred_time})"


class ScheduleSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time_slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course} | {self.term}"


class CourseHistory(models.Model):
    """
    Stores the parsed history from the Google Sheet.
    """

    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    year = models.IntegerField()
    teacher_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.year} - {self.course_name} ({self.teacher_name})"
