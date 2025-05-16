from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EspecialidadViewSet

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)

urlpatterns = router.urls  # 👈 Exporta directamente las rutas del router
