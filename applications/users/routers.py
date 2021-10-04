from rest_framework.routers import DefaultRouter
from . import viewsets

router= DefaultRouter() #definimos el objeto

router.register(r'usersAdmin',viewsets.UserViewSet, basename='admin-user')
router.register(r'groups',viewsets.GroupViewSet, basename='group-user')
router.register(r'permissions',viewsets.PermissionViewSet, basename='permission-user')




urlpatterns = router.urls