from django.db import models

# Create your models here.
class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Dispositivos(models.Model):
    nombre = models.CharField(max_length=100)
    consumo = models.IntegerField()
    estado = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre