from django.urls import path, include  # Esto es necesario
from rest_framework.routers import DefaultRouter
from .views import EspecialidadViewSet

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Esto incluirá todas las rutas generadas automáticamente por el DefaultRouter
]
