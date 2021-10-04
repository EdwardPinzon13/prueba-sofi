from django.urls import path

from . import views
app_name = 'users_app'

urlpatterns = [
    path('login/', views.Login.as_view(),name='Login'),
    path('logout/', views.Logout.as_view(),name='Logout'),
    path('refresh-token/', views.UserToken.as_view(),name='refresh-token'),
    path('refresh-password/', views.RecovryPassword.as_view(),name='refresh-password'),
]