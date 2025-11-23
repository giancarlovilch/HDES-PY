from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.list_view, name='list'),  # /inventory/ -> inventory:list
    path('add/', views.add_view, name='add'),
    path('manage/', views.manage_view, name='manage'),
]