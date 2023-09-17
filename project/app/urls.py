from django.urls import path
from .views import ProcessUrineStrip 
from . import views

urlpatterns = [
    path('process_urinestrip/', ProcessUrineStrip.as_view(), name='process_urinestrip'),
     path('', views.home, name=''),
]
