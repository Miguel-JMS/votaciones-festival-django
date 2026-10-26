from django.contrib import admin

from .models import Categoria, Edicion, Opcion, Voto, Votacion

admin.site.site_header = "Administración – Votaciones Festival Vallenato"
admin.site.site_title = "Votaciones Festival"


class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 0


class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 2


@admin.register(Edicion)
class EdicionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "anio", "fecha_inicio", "fecha_fin", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    inlines = [CategoriaInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edicion", "activa")
    list_filter = ("edicion", "activa")
    search_fields = ("nombre",)


@admin.register(Votacion)
class VotacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "fecha_apertura", "fecha_cierre", "votos_max_por_usuario", "activa")
    list_filter = ("categoria__edicion", "categoria", "activa")
    search_fields = ("titulo",)
    inlines = [OpcionInline]


@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "votacion", "activa")
    list_filter = ("votacion__categoria__edicion", "activa")
    search_fields = ("nombre",)


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    """Solo lectura: los votos no se crean ni se editan desde el admin (RN-05, trazabilidad)."""
    list_display = ("usuario", "votacion", "opcion", "fecha_hora")
    list_filter = ("votacion",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
