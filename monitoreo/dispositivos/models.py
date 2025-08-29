from django.db import models


class Categoria(models.Model):
    nombreCategoria = models.CharField(max_length=45)
    descripcionCategoria = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombreCategoria


class Zona(models.Model):
    nombreZona = models.CharField(max_length=45)
    descripcionZona = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombreZona


class Dispositivo(models.Model):
    nombreDispositivo = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=45)  
    marca = models.CharField(max_length=45)
    potencia = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="dispositivos")
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name="dispositivos")

    def __str__(self):
        return self.nombreDispositivo


class Medicion(models.Model):
    fechaHora = models.DateTimeField()
    consumo = models.FloatField()
    voltaje = models.FloatField()
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name="mediciones")

    def __str__(self):
        return f"{self.dispositivo.nombreDispositivo} - {self.fechaHora}"


class Alerta(models.Model):
    tipoAlerta = models.CharField(max_length=45)
    fechaHora = models.DateTimeField()
    nivelCriticidad = models.CharField(max_length=45)
    descripcionAlerta = models.CharField(max_length=200, blank=True, null=True)

    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name="alertas")

    def __str__(self):
        return f"Alerta {self.tipoAlerta} en {self.dispositivo.nombreDispositivo}"
