from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('user-register/', views.register_view, name='register'),
    path('user-login/', views.login_view, name='login'),
    path('user-logout/', views.logout_view, name='logout'),
    path('user-profile/', views.profile_view, name='profile'),
    path('user-profile-update/', views.update_profile_view, name='update_profile'),
    path('user-profile-delete/', views.delete_profile_view, name="delete_profile"),
]
