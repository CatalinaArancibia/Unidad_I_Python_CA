from dispositivos.models import Organization, Category, Product, Model, Brand, Zone, Device, Measurement, Alert, Product_Alert
from django.contrib.auth.models import User

# Usuarios
user1 = User.objects.create_user(username='ana', email='ana@email.com', password='ana12345')
user2 = User.objects.create_user(username='luis', email='luis@email.com', password='luis12345')
user3 = User.objects.create_user(username='sofia', email='sofia@email.com', password='sofia12345')

# Organizaciones
org1 = Organization.objects.create(organization_name='Empresa Solar', organization_description='Energia renovable')
org2 = Organization.objects.create(organization_name='Industria Fria', organization_description='Refrigeracion industrial')

# Categorias
cat1 = Category.objects.create(category_name='Climatizacion', category_description='Aires acondicionados y calefaccion')
cat2 = Category.objects.create(category_name='Iluminacion', category_description='Luminarias LED')

# Marcas y Modelos
brand1 = Brand.objects.create(brand_name='Samsung', brand_description='Electrodomesticos')
brand2 = Brand.objects.create(brand_name='Philips', brand_description='Iluminacion')

model1 = Model.objects.create(model_name='SP500', model_description='Modelo eficiente', brand_idbrand=brand1)
model2 = Model.objects.create(model_name='LUX100', model_description='Modelo LED', brand_idbrand=brand2)

# Productos
prod1 = Product.objects.create(product_name='Aire Acondicionado', power=1500, category_idcategory=cat1, model_idmodel=model1)
prod2 = Product.objects.create(product_name='Lampara LED', power=20, category_idcategory=cat2, model_idmodel=model2)

# Zonas
zone1 = Zone.objects.create(zone_name='Oficina Central', zone_description='Oficina principal', location='Piso 1', organization=org1)
zone2 = Zone.objects.create(zone_name='Deposito', zone_description='Zona de almacenamiento', location='Subsuelo', organization=org2)

# Dispositivos
device1 = Device.objects.create(device_name='AA-01', category_idcategory=cat1, zone_idzone=zone1, product_idproduct=prod1, organization=org1)
device2 = Device.objects.create(device_name='LED-01', category_idcategory=cat2, zone_idzone=zone2, product_idproduct=prod2, organization=org2)
device3 = Device.objects.create(device_name='AA-02', category_idcategory=cat1, zone_idzone=zone1, product_idproduct=prod1, organization=org1)

# Mediciones
meas1 = Measurement.objects.create(consumption=1600, voltage=220, device_iddevice=device1)
meas2 = Measurement.objects.create(consumption=18, voltage=230, device_iddevice=device2)
meas3 = Measurement.objects.create(consumption=1700, voltage=215, device_iddevice=device3)

# Alertas
alert1 = Alert.objects.create(alert_type='Alto consumo', severity_level='ALTO', message='Consumo elevado detectado', device=device1, measurement=meas1)
alert2 = Alert.objects.create(alert_type='Bajo voltaje', severity_level='MEDIANO', message='Voltaje bajo detectado', device=device3, measurement=meas3)

# Umbrales de alerta para productos
pa1 = Product_Alert.objects.create(product_idproduct=prod1, alert_idalert=alert1, min_value=0, max_value=1500)
pa2 = Product_Alert.objects.create(product_idproduct=prod2, alert_idalert=alert2, min_value=15, max_value=25)

print("Datos de prueba creados exitosamente!")
