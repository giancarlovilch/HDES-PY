from django.urls import path
from . import views

app_name = 'legal'
urlpatterns = [
    path('privacy/', views.privacy_view, name='privacy'),  # /legal/privacy/ -> legal:privacy
    path('terms/', views.terms_view, name='terms'),  # /legal/terms/ -> legal:terms
]