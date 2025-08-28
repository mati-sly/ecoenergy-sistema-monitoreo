from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Categoria, Zona, Dispositivo, Medicion, Alerta

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'created_at']
    search_fields = ['nombre']

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'capacidad_maxima', 'created_at']
    search_fields = ['nombre', 'ubicacion']

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'modelo', 'categoria', 'zona', 'estado', 'potencia_watts']
    list_filter = ['categoria', 'zona', 'estado']
    search_fields = ['nombre', 'modelo']

@admin.register(Medicion)
class MedicionAdmin(admin.ModelAdmin):
    list_display = ['dispositivo', 'consumo_kwh', 'timestamp']
    list_filter = ['timestamp', 'dispositivo__categoria']
    search_fields = ['dispositivo__nombre']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['dispositivo', 'tipo_alerta', 'nivel', 'estado', 'fecha_alerta']
    list_filter = ['tipo_alerta', 'nivel', 'estado', 'fecha_alerta']
    search_fields = ['dispositivo__nombre', 'mensaje']