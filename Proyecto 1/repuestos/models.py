from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Repuesto(models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=100, default='Sin marca')
    modelo_auto = models.CharField(max_length=100, default='Universal')
    año_auto = models.CharField(max_length=4, default='2024')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='repuestos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - {self.modelo_auto} {self.año_auto}"

    class Meta:
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.repuesto.nombre}"

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
