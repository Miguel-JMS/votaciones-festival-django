from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),  # login, logout, cambio de contraseña
    path("", include("votaciones.urls")),
]
