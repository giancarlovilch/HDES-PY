from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.SeatListView.as_view(), name='seat_list'),
    path('reset/', views.reset_assignments, name='reset_assignments'),    
   
    path('workers/', views.WorkerListView.as_view(), name='worker_list'),
    path('workers/create/', views.WorkerCreateView.as_view(), name='worker_create'),
    path('workers/<int:pk>/edit/', views.WorkerUpdateView.as_view(), name='worker_edit'),
    path('workers/<int:pk>/delete/', views.WorkerDeleteView.as_view(), name='worker_delete'),
]