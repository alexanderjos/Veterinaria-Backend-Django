from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EspecialidadViewSet

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
