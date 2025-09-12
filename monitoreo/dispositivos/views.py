from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Zone, Device, Measurement, Alert, Organization, OrganizationUser
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .forms import OrganizationForm, OrganizationLoginForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            org_name = form.cleaned_data['organization_name']
            org_desc = form.cleaned_data.get('organization_description', '')

            user = User.objects.create_user(username=username, email=email, password=password)

            # Normaliza el nombre de la empresa
            org_name_normalized = org_name.strip().lower()

            # Busca si ya existe una empresa con ese nombre (ignorando mayúsculas/minúsculas)
            organization = Organization.objects.filter(organization_name__iexact=org_name_normalized).first()
            if not organization:
                organization = Organization.objects.create(
                    organization_name=org_name_normalized,
                    organization_description=org_desc
                )

            OrganizationUser.objects.create(user=user, organization=organization)

            messages.success(request, 'Usuario registrado exitosamente en la empresa.')
            return redirect('login')
    else:
        form = OrganizationForm()
    return render(request, 'dispositivos/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = OrganizationLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Buscar el usuario por email
                user = User.objects.get(email=email)
                
                # Verificar contraseña
                if user.check_password(password):
                    # Obtener la organización del OrganizationUser
                    org_user = OrganizationUser.objects.get(user=user)
                    request.session['organization_id'] = org_user.organization.id_organization
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except User.DoesNotExist:
                messages.error(request, 'Correo no registrado.')
    else:
        form = OrganizationLoginForm()
    return render(request, 'dispositivos/login.html', {'form': form})

def dashboard(request):
    # Verifica si el usuario está logueado
    if not request.session.get('organization_id'):
        messages.error(request, "Debes iniciar sesión para acceder al dashboard.")
        return redirect('login')
    
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
    if not request.session.get('organization_id'):
        messages.error(request, "Debes iniciar sesión para acceder.")
        return redirect('login')
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
    if not request.session.get('organization_id'):
        messages.error(request, "Debes iniciar sesión para acceder.")
        return redirect('login')
    device = get_object_or_404(Device, id=device_id)
    return render(request, "dispositivos/device_detail.html", {"device": device})

def measurements(request):
    if not request.session.get('organization_id'):
        messages.error(request, "Debes iniciar sesión para acceder.")
        return redirect('login')
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

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            try:
                # Buscar el usuario por email
                user = User.objects.get(email=email)
                
                # Actualizar la contraseña de manera segura
                user.set_password(new_password)
                user.save()
                
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Correo no registrado.')
    else:
        form = PasswordResetForm()
    return render(request, 'dispositivos/passwordreset.html', {'form': form})
def logout(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')
