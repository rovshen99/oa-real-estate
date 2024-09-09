from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.submit_daily_report, name='submit_daily_report'),
]
