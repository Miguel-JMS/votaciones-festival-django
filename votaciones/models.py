from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Edicion(models.Model):
    """Raíz de la jerarquía: permite reutilizar la plataforma cada año."""
    nombre = models.CharField(max_length=120)
    anio = models.PositiveIntegerField("año", unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "edición"
        verbose_name_plural = "ediciones"
        ordering = ["-anio"]

    def __str__(self):
        return f"{self.nombre} ({self.anio})"


class Categoria(models.Model):
    edicion = models.ForeignKey(Edicion, on_delete=models.CASCADE, related_name="categorias")
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["edicion", "nombre"]
        unique_together = [("edicion", "nombre")]

    def __str__(self):
        return f"{self.nombre} – {self.edicion.anio}"


class Votacion(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="votaciones")
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    # Regla pendiente de validación (RN-04): se deja configurable por votación.
    votos_max_por_usuario = models.PositiveSmallIntegerField(default=1)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "votación"
        verbose_name_plural = "votaciones"
        ordering = ["fecha_apertura"]

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_apertura and self.fecha_cierre and self.fecha_cierre <= self.fecha_apertura:
            raise ValidationError("La fecha de cierre debe ser posterior a la de apertura.")

    @property
    def estado(self):
        ahora = timezone.now()
        if not self.activa:
            return "Inactiva"
        if ahora < self.fecha_apertura:
            return "Próxima"
        if ahora > self.fecha_cierre:
            return "Cerrada"
        return "Abierta"


class Opcion(models.Model):
    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE, related_name="opciones")
    nombre = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "opción"
        verbose_name_plural = "opciones"
        ordering = ["votacion", "nombre"]

    def __str__(self):
        return self.nombre


class Voto(models.Model):
    """Preparado para la siguiente entrega (registro definitivo de votos).
    En esta fase solo existe el modelo; aún no hay vistas que lo escriban."""
    votacion = models.ForeignKey(Votacion, on_delete=models.PROTECT, related_name="votos")
    opcion = models.ForeignKey(Opcion, on_delete=models.PROTECT, related_name="votos")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="votos")
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.usuario} → {self.opcion}"

    def clean(self):
        if self.opcion_id and self.votacion_id and self.opcion.votacion_id != self.votacion_id:
            raise ValidationError("La opción no pertenece a la votación indicada.")
