from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.create_employee, name='create_employee'),
    path('employees/get/', views.get_employees, name='get_employees'),
]