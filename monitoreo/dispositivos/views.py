from django.shortcuts import render
from .models import Category, Zone, Device, Measurement, Alert
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    # Resumen por categoría
    categorias = Category.objects.all()
    resumen_categoria = [
        {"nombre": c.category_name, "cantidad": Device.objects.filter(category_idcategory=c).count()}
        for c in categorias
    ]

    # Resumen por zona
    zonas = Zone.objects.all()
    resumen_zona = [
        {"nombre": z.zone_name, "cantidad": Device.objects.filter(zone_idzone=z).count()}
        for z in zonas
    ]

    # Alertas de la semana (ejemplo: últimas 7 días)
    semana = timezone.now() - timedelta(days=7)
    alertas_semana = Alert.objects.filter(created_at__gte=semana)
    resumen_alertas = {
        "GRAVE": alertas_semana.filter(severity_level="GRAVE").count(),
        "ALTO": alertas_semana.filter(severity_level="ALTO").count(),
        "MEDIANO": alertas_semana.filter(severity_level="MEDIANO").count(),
    }

    # Últimas 10 mediciones
    mediciones = Measurement.objects.select_related('device_iddevice').order_by('-created_at')[:10]

    # Últimas 5 alertas
    alertas_recientes = Alert.objects.order_by('-created_at')[:5]

    # Lista de dispositivos
    dispositivos = Device.objects.select_related('category_idcategory', 'zone_idzone').all()[:12]

    context = {
        "resumen_categoria": resumen_categoria,
        "resumen_zona": resumen_zona,
        "resumen_alertas": resumen_alertas,
        "mediciones": mediciones,
        "alertas_recientes": alertas_recientes,
        "dispositivos": dispositivos,
        "categorias": categorias,
        "zonas": zonas,
    }
    return render(request, "dispositivos/dashboard.html", context)
