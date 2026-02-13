from django.contrib import admin
from .models import Teacher, Classroom, Module, ScheduleSlot

admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Module)
admin.site.register(ScheduleSlot)
