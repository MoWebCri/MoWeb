from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Curso(models.Model):
    CATEGORIA_CHOICES = (
        ('programacion', 'Programación'),
        ('diseno', 'Diseño'),
        ('marketing', 'Marketing Digital'),
        ('idiomas', 'Idiomas'),
        ('otros', 'Otros'),
    )
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField(null=True, blank=True, help_text='Contenido detallado del curso')
    precio = models.PositiveIntegerField(help_text='Precio en pesos chilenos')
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='otros', null=True, blank=True)
    duracion = models.PositiveIntegerField(help_text='Duración en horas', null=True, blank=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    enlace_moodle = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.titulo

    def esta_en_carrito(self, usuario):
        if not usuario.is_authenticated:
            return False
        return self.itemcarrito_set.filter(carrito__usuario=usuario).exists()

    def esta_comprado(self, usuario):
        if not usuario.is_authenticated:
            return False
        return self.detallecompra_set.filter(compra__usuario=usuario, compra__estado='completada').exists()

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ('carrito', 'curso')

    def __str__(self):
        return f"{self.curso.titulo} en carrito de {self.carrito.usuario.username}"

    @property
    def subtotal(self):
        return self.curso.precio

class Compra(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cursos = models.ManyToManyField(Curso, through='DetalleCompra')

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-fecha_compra']

    def __str__(self):
        return f"Compra de {self.usuario.username} - {self.fecha_compra.strftime('%d/%m/%Y')}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'

    def __str__(self):
        return f"{self.curso.titulo} en compra {self.compra.id}"
