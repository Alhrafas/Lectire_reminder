from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    CATEGORY_CHOICES = [
        ("math", "Mathematics"),
        ("science", "Science"),
        ("programming", "Programming"),
        ("education", "Education"),
        ("other", "Other"),
    ]

    RECURRING_CHOICES = [
        ('none', 'Does not repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200, help_text="Lecture Venue")
    reminder_time = models.TimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    recurrence = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date} at {self.time})"
