# huellitas/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import EspecialidadViewSet  # Importa el viewset

# Crea un router para manejar las URLs automáticamente
router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)  # Registro del viewset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluye las URLs del router
]
