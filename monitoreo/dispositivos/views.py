from django.shortcuts import render
from .models import Dispositivo

def inicio(request):
    dispositivos = Dispositivo.objects.select_related("categoria")
    return render(request, "dispositivos/inicio.html", {"dispositivos": dispositivos})

def dispositivo(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    return render(request, "dispositivos/detalle.html", {"dispositivo": dispositivo})

# Puedes mantener esta función si la necesitas
def panel_dispositivos(request):
    dispositivos = [
        {"nombre": "Sensor Temperatura", "consumo": 50},
        {"nombre": "Medidor Solar", "consumo": 120},
        {"nombre": "Sensor Movimiento", "consumo": 30},
        {"nombre": "Calefactor", "consumo": 200},
    ]
    consumo_maximo = 100
    return render(
        request,
        "dispositivos/panel.html",
        {"dispositivos": dispositivos, "consumo_maximo": consumo_maximo},
    )