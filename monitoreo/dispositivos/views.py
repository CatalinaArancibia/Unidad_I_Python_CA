from django.shortcuts import render, get_object_or_404
from .models import Category, Zone, Device, Measurement, Alert
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

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

def devices(request):
    categorias = Category.objects.all()
    zonas = Zone.objects.all()
    dispositivos = Device.objects.select_related('category_idcategory', 'zone_idzone').all()

    # Filtros
    categoria_id = request.GET.get('categoria')
    zona_id = request.GET.get('zona')
    search = request.GET.get('search')

    if categoria_id:
        dispositivos = dispositivos.filter(category_idcategory_id=categoria_id)
    if zona_id:
        dispositivos = dispositivos.filter(zone_idzone_id=zona_id)
    if search:
        dispositivos = dispositivos.filter(device_name__icontains=search)

    # Paginación
    paginator = Paginator(dispositivos, 10)  # 10 dispositivos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categorias': categorias,
        'zonas': zonas,
        'dispositivos': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'request': request,
    }
    return render(request, "dispositivos/devices.html", context)

def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    return render(request, "dispositivos/device_detail.html", {"device": device})

def measurements(request):
    mediciones = Measurement.objects.select_related('device_iddevice').order_by('-created_at')
    paginator = Paginator(mediciones, 50)  # 50 mediciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'mediciones': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, "dispositivos/measurements.html", context)
