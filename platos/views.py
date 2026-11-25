from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PlatoCreateForm, PlatoUpdateForm
from .models import Plato


def index(request):
    """Portada con resumen estadístico de la carta y los últimos 4 platos creados."""
    # Calculamos todas las estadísticas en una sola consulta con aggregate()
    resumen = Plato.objects.aggregate(
        total=Count('id'),
        disponibles=Count('id', filter=Q(disponible=True)),
        sin_stock=Count('id', filter=Q(stock=0)),
        precio_promedio=Avg('precio'),
    )
    stats = {
        'total': resumen['total'] or 0,
        'disponibles': resumen['disponibles'] or 0,
        'sin_stock': resumen['sin_stock'] or 0,
        'precio_promedio': round(resumen['precio_promedio'] or 0),
    }
    # Últimos 4 platos agregados al sistema
    destacados = Plato.objects.order_by('-fecha_creacion', '-id')[:4]

    return render(request, 'platos/index.html', {
        'stats': stats,
        'destacados': destacados,
    })


def plato_list(request):
    """Lista paginada de platos con búsqueda por texto (nombre/descripción) y filtro por categoría."""
    platos = Plato.objects.all()

    busqueda = request.GET.get('q', '').strip()
    categoria_actual = request.GET.get('categoria', '').strip()

    if busqueda:
        # Q permite combinar condiciones OR: buscar en nombre o en descripción
        platos = platos.filter(
            Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )
    if categoria_actual:
        platos = platos.filter(categoria=categoria_actual)

    # Paginación de 6 platos por página
    paginator = Paginator(platos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'platos/lista.html', {
        'page_obj': page_obj,
        'platos': page_obj.object_list,
        'busqueda': busqueda,
        'categoria_actual': categoria_actual,
        'categorias': Plato.Categoria.choices,
    })


def plato_detail(request, pk):
    """Muestra el detalle completo de un plato o devuelve error 404 si no existe."""
    plato = get_object_or_404(Plato, pk=pk)
    return render(request, 'platos/detalle.html', {'plato': plato})


def _procesar_formulario(request, form_class, template_name, mensaje_exito, instance=None):
    """
    Función auxiliar compartida por plato_create y plato_update para evitar
    duplicar el manejo de GET/POST, validación y mensajes flash.
    """
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            plato_guardado = form.save()
            messages.success(request, mensaje_exito.format(nombre=plato_guardado.nombre))
            return redirect('platos:lista')
        messages.error(request, 'Por favor corrige los errores indicados en el formulario.')
    else:
        form = form_class(instance=instance)

    return render(request, template_name, {
        'form': form,
        'plato': instance,
    })


def plato_create(request):
    """Crea un nuevo plato usando PlatoCreateForm (disponibilidad automática según stock)."""
    return _procesar_formulario(
        request=request,
        form_class=PlatoCreateForm,
        template_name='platos/crear.html',
        mensaje_exito='El plato "{nombre}" fue creado correctamente.',
    )


def plato_update(request, pk):
    """Edita un plato existente usando PlatoUpdateForm."""
    plato = get_object_or_404(Plato, pk=pk)
    return _procesar_formulario(
        request=request,
        form_class=PlatoUpdateForm,
        template_name='platos/editar.html',
        mensaje_exito='El plato "{nombre}" fue actualizado correctamente.',
        instance=plato,
    )


def plato_delete(request, pk):
    """Muestra confirmación en GET y solo elimina el plato cuando se confirma por POST."""
    plato = get_object_or_404(Plato, pk=pk)

    if request.method == 'POST':
        nombre = plato.nombre
        plato.delete()
        messages.success(request, f'El plato "{nombre}" fue eliminado correctamente.')
        return redirect('platos:lista')

    return render(request, 'platos/eliminar_confirmar.html', {'plato': plato})
