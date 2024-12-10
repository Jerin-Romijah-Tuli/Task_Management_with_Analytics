# tasks/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'start_date', 'end_date', 'status', 'priority', 'category', 'reminder_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Due Date (mm/dd/yyyy)'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Start Date (mm/dd/yyyy)'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'End Date (mm/dd/yyyy)'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'reminder_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Reminder Date (mm/dd/yyyy)'}),
        }
