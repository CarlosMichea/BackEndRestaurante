from django.contrib import admin
from .models import Plato


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    """Configuración del modelo Plato en el panel de administración de Django."""

    list_display = (
        'nombre',
        'categoria',
        'precio',
        'stock',
        'tiempo_preparacion',
        'es_vegetariano',
        'disponible',
    )
    list_filter = ('categoria', 'disponible', 'es_vegetariano')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'disponible')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
