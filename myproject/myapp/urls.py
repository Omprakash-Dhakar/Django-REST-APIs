from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.MyAPIView.as_view(), name='api_view'),
]
