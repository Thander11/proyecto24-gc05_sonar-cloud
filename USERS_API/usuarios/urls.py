from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, PerfilesViewSet, PagoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'perfiles', PerfilesViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('usuarios/buscar/', UsuarioViewSet.as_view({'get': 'buscar'})),
    path('pagos/por_usuario/<int:idUsuario>/', PagoViewSet.as_view({'get': 'por_usuario'})),
    path('perfiles/por_usuario/<int:idUsuario>/', PerfilesViewSet.as_view({'get': 'por_usuario'})),
]
