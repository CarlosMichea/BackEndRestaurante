from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import Plato


WIDGETS_PLATO = {
    'nombre': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: Pastel de choclo',
        'minlength': 3,
        'maxlength': 80,
        'required': 'required',
    }),
    'descripcion': forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Ej: Pastel tradicional chileno con pino de carne y cubierta de choclo.',
        'minlength': 10,
        'required': 'required',
    }),
    'categoria': forms.Select(attrs={
        'class': 'form-select',
        'required': 'required',
    }),
    'precio': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: 9500',
        'min': 1,
        'max': 500000,
        'required': 'required',
    }),
    'stock': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: 15',
        'min': 0,
        'required': 'required',
    }),
    'tiempo_preparacion': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: 25',
        'min': 1,
        'max': 180,
        'required': 'required',
    }),
    'es_vegetariano': forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }),
    'disponible': forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }),
    'imagen_url': forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://ejemplo.com/plato.jpg',
    }),
}

HELP_TEXTS_PLATO = {
    'nombre': 'Nombre único del plato (entre 3 y 80 caracteres).',
    'descripcion': 'Describe brevemente los ingredientes y preparación (mínimo 10 caracteres).',
    'categoria': 'Selecciona a qué sección de la carta pertenece.',
    'precio': 'Valor en pesos chilenos (CLP), entre $1 y $500.000.',
    'stock': 'Cantidad de porciones disponibles (0 o más).',
    'tiempo_preparacion': 'Tiempo estimado de cocina en minutos (entre 1 y 180).',
    'es_vegetariano': 'Marca esta casilla si no contiene carnes ni pescados.',
    'disponible': 'Indica si el plato está activo para la venta.',
    'imagen_url': 'Opcional: enlace http:// o https:// a una fotografía del plato.',
}


class PlatoFormMixin:
    """
    Mixin compartido con las validaciones comunes y marcado Bootstrap 'is-invalid'
    para evitar duplicar lógica entre PlatoCreateForm y PlatoUpdateForm.
    """

    def full_clean(self):
        """Agrega la clase Bootstrap 'is-invalid' a cualquier campo con errores."""
        super().full_clean()
        for nombre_campo in self.errors:
            if nombre_campo in self.fields:
                clases = self.fields[nombre_campo].widget.attrs.get('class', '')
                if 'is-invalid' not in clases:
                    self.fields[nombre_campo].widget.attrs['class'] = f'{clases} is-invalid'.strip()

    def clean_nombre(self):
        """Elimina espacios extra, valida longitud mínima y unicidad sin distinguir mayúsculas."""
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre del plato no puede estar vacío.')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del plato debe tener al menos 3 caracteres.')

        # Buscamos otro plato con el mismo nombre ignorando mayúsculas/minúsculas
        duplicados = Plato.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            # Al editar, excluimos el propio registro para permitir guardar sin cambiar el nombre
            duplicados = duplicados.exclude(pk=self.instance.pk)
        if duplicados.exists():
            raise forms.ValidationError('Ya existe un plato registrado con ese nombre.')

        return nombre

    def clean_precio(self):
        """Valida que el precio sea un entero mayor a 0 y no supere $500.000 CLP."""
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a $0 CLP.')
        if precio > 500000:
            raise forms.ValidationError('El precio no puede superar los $500.000 CLP.')
        return precio

    def clean_stock(self):
        """Valida que el stock sea mayor o igual a 0."""
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError('El stock debe ser mayor o igual a 0.')
        return stock

    def clean_imagen_url(self):
        """Valida que la URL de imagen (si se ingresa) tenga formato web válido (http/https)."""
        imagen_url = (self.cleaned_data.get('imagen_url') or '').strip()
        if imagen_url:
            validador = URLValidator(schemes=['http', 'https'])
            try:
                validador(imagen_url)
            except ValidationError:
                raise forms.ValidationError(
                    'Ingresa una URL válida que comience con http:// o https://.'
                )
        return imagen_url


class PlatoCreateForm(PlatoFormMixin, forms.ModelForm):
    """
    Formulario para crear un plato nuevo.
    No incluye el campo 'disponible', ya que se asigna automáticamente según el stock.
    """

    class Meta:
        model = Plato
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'stock',
            'tiempo_preparacion',
            'es_vegetariano',
            'imagen_url',
        ]
        widgets = WIDGETS_PLATO
        help_texts = HELP_TEXTS_PLATO

    def save(self, commit=True):
        """Asigna disponible=True automáticamente si el stock inicial es mayor a 0."""
        plato = super().save(commit=False)
        plato.disponible = plato.stock > 0
        if commit:
            plato.save()
        return plato


class PlatoUpdateForm(PlatoFormMixin, forms.ModelForm):
    """
    Formulario para editar un plato existente.
    Incluye todos los campos editables, incluyendo 'disponible'.
    """

    class Meta:
        model = Plato
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'stock',
            'tiempo_preparacion',
            'es_vegetariano',
            'disponible',
            'imagen_url',
        ]
        widgets = WIDGETS_PLATO
        help_texts = HELP_TEXTS_PLATO

    def clean(self):
        """Impide marcar un plato como disponible si su stock es 0."""
        cleaned_data = super().clean()
        stock = cleaned_data.get('stock')
        disponible = cleaned_data.get('disponible')

        if stock == 0 and disponible:
            self.add_error(
                'disponible',
                'Un plato con stock 0 no puede quedar marcado como disponible.',
            )
        return cleaned_data
