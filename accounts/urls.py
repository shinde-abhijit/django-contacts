from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
]
