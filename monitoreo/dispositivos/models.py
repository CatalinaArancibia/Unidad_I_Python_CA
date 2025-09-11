from django.db import models

# -----------------------------
# Modelo Base con atributos comunes
# -----------------------------

class BaseModel(models.Model):
    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]
    
    status = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVO")
    created_at = models.DateTimeField(auto_now_add=True)  # se asigna al crear
    updated_at = models.DateTimeField(auto_now=True)  # se actualiza cada vez que se guarda
    deleted_at = models.DateTimeField(null=True, blank=True)  # opcional para borrado lógico
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)  # Relación con Organization

    class Meta:
        abstract = True  # no crea tabla, solo se hereda


# ------------------------------
# Tablas principales
# ------------------------------

class Organization(models.Model):
    id_organization = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    organization_description = models.TextField()
    status = models.CharField(max_length=10, choices=BaseModel.ESTADOS, default="ACTIVO")  # Usar ESTADOS de BaseModel
    created_at = models.DateTimeField(auto_now_add=True)  # se asigna al crear
    updated_at = models.DateTimeField(auto_now=True)  # se actualiza cada vez que se guarda
    deleted_at = models.DateTimeField(null=True, blank=True)  # opcional para borrado lógico

    def __str__(self):
        return self.organization_name


class Category(BaseModel):
    category_name = models.CharField(max_length=45)
    category_description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.category_name


class Product(BaseModel):
    product_name = models.CharField(max_length=45)
    power = models.FloatField()
    category_idcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    model_idmodel = models.ForeignKey('Model', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Device(BaseModel):
    device_name = models.CharField(max_length=45)
    category_idcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    zone_idzone = models.ForeignKey('Zone', on_delete=models.CASCADE)

    def __str__(self):
        return self.device_name


class Measurement(BaseModel):
    consumption = models.FloatField()
    voltage = models.FloatField()
    device_iddevice = models.ForeignKey(Device, on_delete=models.CASCADE)
    alert_idalert = models.ForeignKey('Alert', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device_iddevice.device_name} - {self.date_time}"


class Alert(BaseModel):
    alert_type = models.CharField(max_length=45)
    severity_level = models.CharField(
        max_length=10,
        choices=[('MEDIANO', 'Mediano'), ('ALTO', 'Alto'), ('GRAVE', 'Grave')],
        default='MEDIANO'
    )
    message = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Alert {self.alert_type} on {self.date_time}"


class Product_Alert(models.Model):
    product_idproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    alert_idalert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    min_value = models.FloatField()
    max_value = models.FloatField()

    class Meta:
        unique_together = ['product_idproduct', 'alert_idalert']  # Asegura que no haya duplicados de la relación

    def __str__(self):
        return f"Alert {self.alert_idalert.alert_type} for Product {self.product_idproduct.product_name}"

class Model(BaseModel):
    model_name = models.CharField(max_length=45)
    model_description = models.CharField(max_length=200, blank=True, null=True)
    
    # Relación de muchos a uno, un modelo tiene una marca
    brand_idbrand = models.ForeignKey('Brand', on_delete=models.CASCADE)  # Relación entre Modelo y Marca

    def __str__(self):
        return self.model_name
    
class Brand(BaseModel):
    brand_name = models.CharField(max_length=45)
    brand_description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.brand_name
    

class Zone(BaseModel):
    zone_name = models.CharField(max_length=45)
    zone_description = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.zone_name
