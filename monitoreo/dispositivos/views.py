from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Device, Category, Zone, Measurement, Alert, Organization
from .forms import DeviceForm
from django.contrib.auth.decorators import login_required

def get_user_organization(user):
    """Obtiene la organización del usuario logueado"""
    try:
        return Organization.objects.get(email=user.email)
    except Organization.DoesNotExist:
        # Fallback: usar la primera organización disponible
        return Organization.objects.first()

# Dashboard principal - requerido por la evaluación
@login_required
def dashboard(request):
    organization = get_user_organization(request.user)
    
    if organization:
        # Últimas 10 mediciones
        latest_measurements = Measurement.objects.filter(
            organization=organization
        ).select_related('device').order_by('-timestamp')[:10]
        
        # Dispositivos por categoría (conteo)
        devices_by_category = {}
        categories = Category.objects.filter(organization=organization)
        for category in categories:
            count = Device.objects.filter(category=category, organization=organization).count()
            devices_by_category[category.name] = count
        
        # Dispositivos por zona (conteo)
        devices_by_zone = {}
        zones = Zone.objects.filter(organization=organization)
        for zone in zones:
            count = Device.objects.filter(zone=zone, organization=organization).count()
            devices_by_zone[zone.name] = count
        
        # Alertas de la semana por severidad
        week_ago = timezone.now() - timedelta(days=7)
        alerts_by_severity = {}
        severities = ['Grave', 'Alto', 'Mediano']
        for severity in severities:
            count = Alert.objects.filter(
                organization=organization,
                alert_date__gte=week_ago,
                severity=severity
            ).count()
            alerts_by_severity[severity] = count
    else:
        latest_measurements = []
        devices_by_category = {}
        devices_by_zone = {}
        alerts_by_severity = {}
    
    context = {
        'latest_measurements': latest_measurements,
        'devices_by_category': devices_by_category,
        'devices_by_zone': devices_by_zone,
        'alerts_by_severity': alerts_by_severity,
    }
    return render(request, "dispositivos/dashboard.html", context)

# Listado de dispositivos con filtro por categoría
@login_required
def device_list(request):
    organization = get_user_organization(request.user)
    
    devices = Device.objects.filter(organization=organization).select_related("category", "zone")
    categories = Category.objects.filter(organization=organization)
    
    # Filtro por categoría
    category_filter = request.GET.get('category')
    if category_filter:
        devices = devices.filter(category__id=category_filter)
    
    context = {
        'devices': devices,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, "dispositivos/device_list.html", context)

# Detalle de dispositivo con mediciones y alertas
@login_required
def device_detail(request, device_id):
    organization = get_user_organization(request.user)
    device = get_object_or_404(Device, id=device_id, organization=organization)
    
    # Mediciones del dispositivo
    measurements = Measurement.objects.filter(device=device).order_by('-timestamp')[:20]
    
    # Alertas del dispositivo
    alerts = Alert.objects.filter(device=device).order_by('-alert_date')[:10]
    
    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    }
    return render(request, "dispositivos/device_detail.html", context)

# Listado global de mediciones
@login_required
def measurement_list(request):
    organization = get_user_organization(request.user)
    
    measurements = Measurement.objects.filter(
        organization=organization
    ).select_related('device').order_by('-timestamp')[:50]
    
    context = {
        'measurements': measurements,
    }
    return render(request, "dispositivos/measurement_list.html", context)

# Resumen de alertas de la semana
@login_required
def alert_summary(request):
    organization = get_user_organization(request.user)
    week_ago = timezone.now() - timedelta(days=7)
    
    # Alertas de la semana por severidad
    alerts_by_severity = {}
    severities = ['Grave', 'Alto', 'Mediano']
    for severity in severities:
        alerts = Alert.objects.filter(
            organization=organization,
            alert_date__gte=week_ago,
            severity=severity
        ).order_by('-alert_date')
        alerts_by_severity[severity] = alerts
    
    # Alertas recientes
    recent_alerts = Alert.objects.filter(
        organization=organization,
        alert_date__gte=week_ago
    ).select_related('device').order_by('-alert_date')[:10]
    
    context = {
        'alerts_by_severity': alerts_by_severity,
        'recent_alerts': recent_alerts,
    }
    return render(request, "dispositivos/alert_summary.html", context)

# Funciones CRUD manteniendo compatibilidad
@login_required
def inicio(request):
    return dashboard(request)

@login_required
def dispositivo(request, dispositivo_id):
    return device_detail(request, dispositivo_id)

# Esta vista no necesita login porque es datos estáticos
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

# CRUD para dispositivos
@login_required
def crear_dispositivo(request):
    organization = get_user_organization(request.user)
    
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.organization = organization
            device.save()
            return redirect('dashboard')
    else:
        form = DeviceForm()
    return render(request, 'dispositivos/crear.html', {'form': form})

@login_required
def editar_dispositivo(request, dispositivo_id):
    organization = get_user_organization(request.user)
    device = get_object_or_404(Device, id=dispositivo_id, organization=organization)
    
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', device_id=device.id)
    else:
        form = DeviceForm(instance=device)
    
    return render(request, 'dispositivos/editar.html', {'form': form, 'device': device})

@login_required
def eliminar_dispositivo(request, dispositivo_id):
    organization = get_user_organization(request.user)
    device = get_object_or_404(Device, id=dispositivo_id, organization=organization)
    
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard')
    
    return render(request, 'dispositivos/eliminar.html', {'device': device})