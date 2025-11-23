from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("employees/", views.employees_list, name="employees_list"),
    path("schedule/", views.schedule_list, name="schedule_list"),
    path("skills/", views.skills_list, name="skills_list"),
    path("skills/assign/", views.assign_skill, name="assign_skill"),
    path("workers/<int:worker_id>/profile/", views.worker_profile, name="worker_profile"),
    path("reports/", views.reports_list, name="reports_list"),
    path("reports/<int:pk>/", views.report_detail, name="report_detail"),
    path("php/login/", views.php_login, name="php_login"),


]
