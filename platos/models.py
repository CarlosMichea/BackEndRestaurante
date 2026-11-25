from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models


class Plato(models.Model):
    """Modelo que representa un plato dentro de la carta del restaurante."""

    class Categoria(models.TextChoices):
        """Opciones de categoría usando TextChoices de Django."""
        ENTRADA = 'entrada', 'Entrada'
        PLATO_FONDO = 'fondo', 'Plato de fondo'
        ACOMPANAMIENTO = 'acompanamiento', 'Acompañamiento'
        POSTRE = 'postre', 'Postre'
        BEBIDA = 'bebida', 'Bebida'

    nombre = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(3, message='El nombre debe tener al menos 3 caracteres.')],
        verbose_name='Nombre',
    )
    descripcion = models.TextField(
        validators=[MinLengthValidator(10, message='La descripción debe tener al menos 10 caracteres.')],
        verbose_name='Descripción',
    )
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.PLATO_FONDO,
        verbose_name='Categoría',
    )
    # Precio expresado en pesos chilenos (CLP)
    precio = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='El precio mínimo es $1 CLP.'),
            MaxValueValidator(500000, message='El precio máximo permitido es $500.000 CLP.'),
        ],
        verbose_name='Precio (CLP)',
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message='El stock no puede ser negativo.')],
        verbose_name='Stock disponible',
    )
    tiempo_preparacion = models.IntegerField(
        validators=[
            MinValueValidator(1, message='El tiempo mínimo de preparación es 1 minuto.'),
            MaxValueValidator(180, message='El tiempo máximo de preparación es 180 minutos.'),
        ],
        verbose_name='Tiempo de preparación (min)',
    )
    es_vegetariano = models.BooleanField(
        default=False,
        verbose_name='¿Es vegetariano?',
    )
    disponible = models.BooleanField(
        default=True,
        verbose_name='Disponible',
    )
    imagen_url = models.URLField(
        blank=True,
        verbose_name='URL de imagen',
    )
    # Auditoría automática de fechas
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización',
    )

    class Meta:
        verbose_name = 'Plato'
        verbose_name_plural = 'Platos'
        ordering = ['nombre']

    def __str__(self):
        # Representación legible del objeto en el admin y consola
        return f'{self.nombre} (${self.precio})'
