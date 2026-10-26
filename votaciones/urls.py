from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ediciones/<int:pk>/", views.edicion_detalle, name="edicion"),
    path("categorias/<int:pk>/", views.categoria_detalle, name="categoria"),
    path("votaciones/<int:pk>/", views.votacion_detalle, name="votacion"),
    path("registro/", views.registro, name="registro"),
]
