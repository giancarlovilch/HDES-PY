from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('', views.register_view, name='register'),  # /sales/ -> sales:register (página raíz del módulo ventas)
    path('reports/', views.reports_view, name='reports'),  # /sales/reports/ -> sales:reports
    path('history/', views.history_view, name='history'),  # /sales/history/ -> sales:history
]