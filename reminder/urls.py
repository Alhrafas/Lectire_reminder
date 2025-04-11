# reminder/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path("calendar/", views.calendar_view, name="calendar_view"),
    path('api/lectures/', views.lecture_api, name='lecture_api'),
    path('add/', views.add_lecture, name='add_lecture'),
    path('edit/<int:pk>/', views.edit_lecture, name='edit_lecture'),
    path('delete/<int:pk>/', views.delete_lecture, name='delete_lecture'),
    path('register/', views.register, name='register'),  # Added register here
]