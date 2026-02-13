from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    availability_start = models.DateField(null=True, blank=True)
    availability_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(help_text="Max students")
    has_projector = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Cap: {self.capacity})"


class Module(models.Model):
    name = models.CharField(max_length=100)
    duration_weeks = models.IntegerField(default=3)
    is_core = models.BooleanField(default=True)
    # Self-referential ManyToMany for prerequisites (e.g., Module B needs Module A)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.name


class ScheduleSlot(models.Model):
    """
    The 'solution' to the scheduling problem.
    It links a Module to a Teacher, Room, and Time.
    """

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.module} - {self.start_date}"
