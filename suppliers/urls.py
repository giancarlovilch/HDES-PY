from django.urls import path
from . import views

app_name = 'suppliers'
urlpatterns = [
    path('', views.list_view, name='list'),  # /suppliers/ -> suppliers:list
]