from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'productos', ProductoViewSet) 
urlpatterns = router.urls