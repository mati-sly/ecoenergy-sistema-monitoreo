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




# AGREGARÉ clase Medicion y Alerta (Alma):

class Medicion(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='mediciones')
    consumo_kwh = models.DecimalField(max_digits=10, decimal_places=3)
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.dispositivo.nombre} - {self.consumo_kwh} kWh"
    
    class Meta:
        verbose_name_plural = "Mediciones"
        ordering = ['-timestamp']

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('consumo_alto', 'Consumo Alto'),
        ('dispositivo_offline', 'Dispositivo Offline'),
        ('limite_zona', 'Límite de Zona Superado'),
    ]
    
    NIVEL_CHOICES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('critical', 'Crítico'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('resuelta', 'Resuelta'),
        ('descartada', 'Descartada'),
    ]
    
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='alertas')
    tipo_alerta = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    fecha_alerta = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activa')
    
    def __str__(self):
        return f"Alerta {self.nivel} - {self.dispositivo.nombre}"
    
    class Meta:
        ordering = ['-fecha_alerta']
        
