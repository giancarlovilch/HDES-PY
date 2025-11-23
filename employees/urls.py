from django.urls import path
from . import views

app_name = 'employees'
urlpatterns = [
    path('', views.list_view, name='list'),  # /employees/ -> employees:list
    path('add/', views.add_view, name='add'),  # /employees/add/ -> employees:add
]