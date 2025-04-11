from celery import shared_task
from reminder.firebase import send_push_notification

@shared_task
def send_lecture_push_notification(token, lecture_title, lecture_time):
    body = f"Don't forget: {lecture_title} at {lecture_time.strftime('%I:%M %p')}!"
    send_push_notification(token=token, title="Upcoming Lecture", body=body)
