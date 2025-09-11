from django.shortcuts import render
from .models import Measurement, Alert, Device, Category
from datetime import timedelta
from django.utils import timezone

def dashboard(request):
    # Últimas 10 mediciones
    last_measurements = Measurement.objects.all().order_by('-created_at')[:10]
    
    # Alertas de la semana
    one_week_ago = timezone.now() - timedelta(weeks=1)
    weekly_alerts = Alert.objects.filter(created_at__gte=one_week_ago)
    
    # Listado de dispositivos con filtro por categoría
    category_filter = request.GET.get('category')
    devices = Device.objects.all()
    
    if category_filter:
        devices = devices.filter(category_idcategory__category_name=category_filter)
    
    # Obtener todas las categorías para el filtro
    categories = Category.objects.all()
    
    # Pasar toda la información al template
    context = {
        'last_measurements': last_measurements,
        'weekly_alerts': weekly_alerts,
        'devices': devices,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)
