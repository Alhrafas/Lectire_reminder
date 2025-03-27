from django.contrib import admin
from . models import Lecture

# Register your models here.

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'venue', 'reminder_time', 'is_recurring')
