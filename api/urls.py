from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'productos', ProductoViewSet) 
router.register(r'mascotas', MascotaViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'consultorios', ConsultorioViewSet)
router.register(r'tipos-documento', TipoDocumentoViewSet)
router.register(r'trabajadores', TrabajadorViewSet)
router.register(r'veterinarios', VeterinarioViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'citas', CitaViewSet)

urlpatterns = router.urls
