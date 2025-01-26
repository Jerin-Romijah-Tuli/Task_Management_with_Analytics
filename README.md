# Task Manager Project

## Overview

This is a **Task Manager Application** built using the Django framework. The application helps users manage their tasks efficiently by providing features like task creation, updates, filtering, notifications, and analytics.

---

## Features

1. **User Authentication**:

   - Users can register and log in securely with hashed passwords managed by Django's built-in authentication system.
   - Each user has a separate profile, ensuring data privacy and personalized experiences.

![Image](https://github.com/user-attachments/assets/9162d704-fe6e-4927-a88f-ed342bd3d911)
![Image](https://github.com/user-attachments/assets/8d46e1f5-cfd3-4cf1-b7ad-d15e6ae98bdc)


1. **Task Management**:

   - **Create Tasks**: Add new tasks with titles, descriptions, due dates, and priorities.
   - **Update Tasks**: Modify existing tasks to reflect changes in status, priority, or details.
   - **Delete Tasks**: Remove tasks permanently when they are no longer needed.
   - **Due Dates**: Set deadlines to keep track of when tasks need to be completed.
   - **Filtering Options**: Sort and view tasks by their completion status (e.g., pending, completed) and priority (high, medium, low).

![Image](https://github.com/user-attachments/assets/00d9536b-1c3a-4fbe-83f0-e80d52de82d6)
![Image](https://github.com/user-attachments/assets/bc845c7a-4751-48e8-80ce-b0cf85de6dd6)

1. **Analytics and Visualization**:

   - **Pie Chart Representation**: Visualize the ratio of completed vs. pending tasks, giving an instant snapshot of productivity.
   - **Efficiency Calculation**: Measure efficiency as a percentage based on completed tasks versus total tasks.

![Image](https://github.com/user-attachments/assets/3a77b412-24cd-4416-bc18-f6dfdeb3ba20)


1. **Notifications**:

   - **Email Alerts**: Receive automatic email notifications for overdue tasks, ensuring nothing is missed.
   - **Background Scheduler**: A Celery-based periodic task scheduler runs every 10 minutes to check for overdue tasks and send notifications.

![Image](https://github.com/user-attachments/assets/d051a5b8-23b2-4595-9c7f-5d0337d78ec1)


1. **Advanced Features** (Planned):

   - **Kanban Boards**: Intuitive drag-and-drop task management for enhanced workflow visualization.
   - **Calendar Integration**: Sync tasks with a calendar to stay on top of deadlines.
   - **AI-Powered Suggestions**: Smart recommendations for prioritizing and managing tasks more effectively.
   - **Comprehensive Reporting**: Generate detailed reports to analyze task completion trends and productivity over time.



---

## Installation

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- mySql

### Steps

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd Project
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser for the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

1. **Run Background Scheduler**: To enable email notifications for overdue tasks, run the Celery worker:

   ```bash
   celery -A Project worker --loglevel=info
   ```

2. **Scheduled Tasks**: Start the periodic task scheduler:

   ```bash
   celery -A Project beat --loglevel=info
   ```

3. **Access Admin Panel**: Manage tasks and users at: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Project Structure

```
Project/
├── mySql            # SQLite database file
├── manage.py              # Django project entry point
├── requirements.txt       # Python dependencies
├── taskmanager/           # Core Django application
├── tasks/                 # Task management application
├── users/                 # User management application
├── media/                 # Uploaded media files
├── celerybeat-schedule.*  # Celery periodic task files
└── logs/django.log        # Log files for debugging
```

---

## Future Improvements

- Implement Kanban boards for task visualization.
- Add AI-powered suggestions for task prioritization.
- Provide integration with Google Calendar.
- Extend analytics with advanced reporting features.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

- **Django Framework**: [https://www.djangoproject.com/](https://www.djangoproject.com/)
- **Celery**: [https://docs.celeryproject.org/](https://docs.celeryproject.org/)
- **Chart.js**: Used for task analytics visualization.

