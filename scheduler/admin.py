from django.contrib import admin
from .models import Teacher, Classroom, Term, Course, ScheduleSlot

admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(ScheduleSlot)
