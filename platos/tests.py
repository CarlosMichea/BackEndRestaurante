from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .forms import PlatoCreateForm, PlatoUpdateForm
from .models import Plato


def _datos_plato_valido(**overrides):
    """Devuelve un diccionario base válido para probar formularios y vistas."""
    datos = {
        'nombre': 'Cazuela de vacuno',
        'descripcion': 'Caldo tradicional chileno con carne, zapallo, papa y choclo.',
        'categoria': Plato.Categoria.PLATO_FONDO,
        'precio': 8900,
        'stock': 10,
        'tiempo_preparacion': 30,
        'es_vegetariano': False,
        'imagen_url': 'https://ejemplo.com/cazuela.jpg',
    }
    datos.update(overrides)
    return datos


class PlatoFormValidacionesTest(TestCase):
    """Pruebas unitarias de validaciones para PlatoCreateForm y PlatoUpdateForm."""

    def setUp(self):
        self.plato_existente = Plato.objects.create(
            nombre='Pastel de choclo',
            descripcion='Pastel chileno tradicional con pino de carne y choclo molido.',
            categoria=Plato.Categoria.PLATO_FONDO,
            precio=9800,
            stock=5,
            tiempo_preparacion=35,
            disponible=True,
        )

    def test_precio_cero_invalido(self):
        form = PlatoCreateForm(data=_datos_plato_valido(precio=0))
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_precio_negativo_invalido(self):
        form = PlatoCreateForm(data=_datos_plato_valido(precio=-1500))
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_stock_negativo_invalido(self):
        form = PlatoCreateForm(data=_datos_plato_valido(stock=-1))
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_nombre_duplicado_sin_distinguir_mayusculas(self):
        form = PlatoCreateForm(data=_datos_plato_valido(nombre='  pastel DE choclo  '))
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_nombre_corto_invalido(self):
        form = PlatoCreateForm(data=_datos_plato_valido(nombre='Ab'))
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_url_invalida(self):
        form = PlatoCreateForm(data=_datos_plato_valido(imagen_url='no-es-una-url'))
        self.assertFalse(form.is_valid())
        self.assertIn('imagen_url', form.errors)

    def test_update_stock_cero_con_disponible_invalido(self):
        datos = _datos_plato_valido(
            nombre=self.plato_existente.nombre,
            stock=0,
            disponible=True,
        )
        form = PlatoUpdateForm(data=datos, instance=self.plato_existente)
        self.assertFalse(form.is_valid())
        self.assertIn('disponible', form.errors)

    def test_create_form_asigna_disponible_segun_stock(self):
        form_con_stock = PlatoCreateForm(data=_datos_plato_valido(nombre='Humitas', stock=4))
        self.assertTrue(form_con_stock.is_valid())
        plato_con_stock = form_con_stock.save()
        self.assertTrue(plato_con_stock.disponible)

        form_sin_stock = PlatoCreateForm(data=_datos_plato_valido(nombre='Porotos', stock=0))
        self.assertTrue(form_sin_stock.is_valid())
        plato_sin_stock = form_sin_stock.save()
        self.assertFalse(plato_sin_stock.disponible)

    def test_update_permite_mantener_propio_nombre(self):
        datos = _datos_plato_valido(
            nombre='Pastel de choclo',
            precio=10200,
            stock=5,
            disponible=True,
        )
        form = PlatoUpdateForm(data=datos, instance=self.plato_existente)
        self.assertTrue(form.is_valid())


class PlatoCRUDViewsTest(TestCase):
    """Pruebas de integración para todas las vistas CRUD y el index."""

    def setUp(self):
        self.plato = Plato.objects.create(
            nombre='Charquicán',
            descripcion='Guiso tradicional chileno con papas, zapallo y carne.',
            categoria=Plato.Categoria.PLATO_FONDO,
            precio=7900,
            stock=8,
            tiempo_preparacion=20,
            disponible=True,
        )

    def test_index_muestra_estadisticas_y_destacados(self):
        respuesta = self.client.get(reverse('platos:index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['stats']['total'], 1)
        self.assertEqual(respuesta.context['stats']['disponibles'], 1)
        self.assertEqual(respuesta.context['stats']['sin_stock'], 0)
        self.assertEqual(respuesta.context['stats']['precio_promedio'], 7900)
        self.assertIn(self.plato, respuesta.context['destacados'])

    def test_crear_plato_get_y_post(self):
        respuesta_get = self.client.get(reverse('platos:crear'))
        self.assertEqual(respuesta_get.status_code, 200)
        self.assertTemplateUsed(respuesta_get, 'platos/crear.html')

        respuesta_post = self.client.post(
            reverse('platos:crear'),
            data=_datos_plato_valido(nombre='Sopaipillas pasadas', categoria=Plato.Categoria.POSTRE),
        )
        self.assertRedirects(respuesta_post, reverse('platos:lista'))
        self.assertTrue(Plato.objects.filter(nombre='Sopaipillas pasadas').exists())

    def test_listar_platos_busqueda_filtro_y_paginacion(self):
        # Creamos platos extra para probar búsqueda y paginación (> 6 registros)
        for i in range(7):
            Plato.objects.create(
                nombre=f'Entrada especial {i}',
                descripcion='Entrada preparada diariamente con ingredientes frescos.',
                categoria=Plato.Categoria.ENTRADA,
                precio=3000 + i * 100,
                stock=10,
                tiempo_preparacion=10,
                disponible=True,
            )

        respuesta_p1 = self.client.get(reverse('platos:lista'))
        self.assertEqual(respuesta_p1.status_code, 200)
        self.assertEqual(len(respuesta_p1.context['platos']), 6)
        self.assertTrue(respuesta_p1.context['page_obj'].has_next())

        respuesta_p2 = self.client.get(reverse('platos:lista'), {'page': 2})
        self.assertEqual(respuesta_p2.status_code, 200)
        self.assertEqual(len(respuesta_p2.context['platos']), 2)

        # Filtro por búsqueda q en descripción
        respuesta_q = self.client.get(reverse('platos:lista'), {'q': 'zapallo'})
        self.assertQuerySetEqual(respuesta_q.context['platos'], [self.plato])

        # Filtro por categoría
        respuesta_cat = self.client.get(
            reverse('platos:lista'),
            {'categoria': Plato.Categoria.PLATO_FONDO},
        )
        self.assertQuerySetEqual(respuesta_cat.context['platos'], [self.plato])

    def test_detalle_plato_existente_y_404(self):
        respuesta = self.client.get(reverse('platos:detalle', args=[self.plato.pk]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'platos/detalle.html')
        self.assertContains(respuesta, self.plato.nombre)

        respuesta_404 = self.client.get(reverse('platos:detalle', args=[9999]))
        self.assertEqual(respuesta_404.status_code, 404)

    def test_editar_plato_get_y_post(self):
        url_editar = reverse('platos:editar', args=[self.plato.pk])
        respuesta_get = self.client.get(url_editar)
        self.assertEqual(respuesta_get.status_code, 200)
        self.assertTemplateUsed(respuesta_get, 'platos/editar.html')

        respuesta_post = self.client.post(
            url_editar,
            data=_datos_plato_valido(
                nombre='Charquicán con huevo',
                precio=8500,
                stock=0,
                disponible=False,
            ),
        )
        self.assertRedirects(respuesta_post, reverse('platos:lista'))
        self.plato.refresh_from_db()
        self.assertEqual(self.plato.nombre, 'Charquicán con huevo')
        self.assertEqual(self.plato.precio, 8500)
        self.assertEqual(self.plato.stock, 0)
        self.assertFalse(self.plato.disponible)

    def test_eliminar_plato_get_y_post(self):
        url_eliminar = reverse('platos:eliminar', args=[self.plato.pk])
        respuesta_get = self.client.get(url_eliminar)
        self.assertEqual(respuesta_get.status_code, 200)
        self.assertTemplateUsed(respuesta_get, 'platos/eliminar_confirmar.html')
        # GET nunca debe eliminar el registro
        self.assertTrue(Plato.objects.filter(pk=self.plato.pk).exists())

        respuesta_post = self.client.post(url_eliminar)
        self.assertRedirects(respuesta_post, reverse('platos:lista'))
        self.assertFalse(Plato.objects.filter(pk=self.plato.pk).exists())


class SeedPlatosCommandTest(TestCase):
    """Prueba que el comando seed_platos crea 12 platos y es idempotente."""

    def test_seed_platos_crea_12_y_no_duplica(self):
        call_command('seed_platos')
        self.assertEqual(Plato.objects.count(), 12)
        self.assertTrue(Plato.objects.filter(stock=0).exists())

        call_command('seed_platos')
        self.assertEqual(Plato.objects.count(), 12)
