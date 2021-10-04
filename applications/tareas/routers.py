from rest_framework.routers import DefaultRouter
from . import viewsets

router= DefaultRouter() #definimos el objeto

router.register(r'activity',viewsets.ActivityViewSet, basename='activity'),
router.register(r'State',viewsets.StateViewSet, basename='activityState'),



urlpatterns = router.urls

