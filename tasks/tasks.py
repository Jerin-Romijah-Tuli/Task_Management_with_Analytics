from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

def send_task_reminders():
    now = timezone.now()
    # Filter for tasks that are overdue and not completed
    overdue_tasks = Task.objects.filter(due_date__lte=now).exclude(status='completed')
    
    for task in overdue_tasks:
        send_mail(
            subject=f"Reminder: {task.title} is overdue",
            message=f"Your task '{task.title}' was due on {task.due_date}. Please take necessary action.",
            from_email='taskmanager056@gmail.com',
            recipient_list=[task.user.email],
        )
        
        # Optional: You can update a 'notified' field if you want to track reminders sent
        # task.notified = True
        task.save()
