from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

class Zona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=200)
    capacidad_maxima = models.DecimalField(max_digits=10, decimal_places=2, help_text="Capacidad máxima en kW")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"

class Dispositivo(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=150)
    modelo = models.CharField(max_length=100)
    potencia_watts = models.PositiveIntegerField(help_text="Potencia en watts")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='dispositivos')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='dispositivos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    consumo = models.IntegerField(help_text="Consumo actual en watts")  # Mantengo tu campo original
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nombre} ({self.modelo}) - {self.zona.nombre}"
    
    class Meta:
        unique_together = ['nombre', 'zona']  # No permitir nombres duplicados en la misma zona

# AQUÍ ALMA AGREGARÁ SUS MODELOS:
# - Medicion 
# - Alerta