from django.contrib import admin
from django.urls import path, include
from users.views import login_view, register, dashboard, home, custom_logout_view,request_password_reset,confirm_password_reset
from tasks.views import analytics_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('', home, name='home'),  # Home view
    path('login/', login_view, name='login'),  # Login view
    path('register/', register, name='register'),
    path("password-reset/", request_password_reset, name="password_reset"),  # Change to match your desired URL
    path("confirm-password-reset/", confirm_password_reset, name="confirm_password_reset"),  # Consistent naming  # Shorter path for confirmation
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard view (from users app)
    path('tasks/', include('tasks.urls')),  # Include task-related routes
    path('analytics-data/', analytics_data, name='analytics_data'),  # Analytics Data endpoint
    path('logout/', custom_logout_view, name='logout'),  # Logout view
]
