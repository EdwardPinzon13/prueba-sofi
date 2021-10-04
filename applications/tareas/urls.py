from django.urls import path

from . import views
app_name = 'tareas_app'

urlpatterns = [
    path('activitiesHome/', views.ActivityListAPIView.as_view(),name='activitiesHome'),
    path('activities-To-Finish/', views.ActivityToFinishListAPIView.as_view(),name='activitiesToFinish'),

]