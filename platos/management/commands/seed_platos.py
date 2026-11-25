from django.core.management.base import BaseCommand
from platos.models import Plato


class Command(BaseCommand):
    """Comando de Django para poblar la base de datos con 12 platos de ejemplo."""

    help = 'Carga 12 platos realistas en la base de datos sin duplicar registros existentes.'

    def handle(self, *args, **options):
        # 12 platos de ejemplo repartidos entre todas las categorías del restaurante
        platos_ejemplo = [
            {
                'nombre': 'Empanada de pino',
                'descripcion': 'Empanada tradicional horneada rellena de carne picada, cebolla, huevo duro y aceituna.',
                'categoria': Plato.Categoria.ENTRADA,
                'precio': 3200,
                'stock': 25,
                'tiempo_preparacion': 15,
                'es_vegetariano': False,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Ceviche mixto',
                'descripcion': 'Pescado fresco y mariscos marinados en jugo de limón con cebolla morada y cilantro.',
                'categoria': Plato.Categoria.ENTRADA,
                'precio': 7800,
                'stock': 12,
                'tiempo_preparacion': 15,
                'es_vegetariano': False,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Sopaipillas con pebre',
                'descripcion': 'Cuatro sopaipillas caseras de zapallo acompañadas con pebre chileno tradicional.',
                'categoria': Plato.Categoria.ENTRADA,
                'precio': 3500,
                'stock': 30,
                'tiempo_preparacion': 10,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Pastel de choclo',
                'descripcion': 'Clásico pastel chileno en librillo de greda con pino de carne, pollo y cubierta de choclo.',
                'categoria': Plato.Categoria.PLATO_FONDO,
                'precio': 9800,
                'stock': 14,
                'tiempo_preparacion': 35,
                'es_vegetariano': False,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Lomo a lo pobre',
                'descripcion': 'Lomo liso a la plancha servido con papas fritas caseras, cebolla caramelizada y huevos.',
                'categoria': Plato.Categoria.PLATO_FONDO,
                'precio': 13500,
                'stock': 10,
                'tiempo_preparacion': 25,
                'es_vegetariano': False,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Salmón a la plancha',
                'descripcion': 'Filete de salmón grillado al limón con hierbas frescas y salsa de alcaparras.',
                'categoria': Plato.Categoria.PLATO_FONDO,
                'precio': 14200,
                'stock': 0,  # Plato sin stock para demostrar el estado agotado
                'tiempo_preparacion': 22,
                'es_vegetariano': False,
                'disponible': False,
                'imagen_url': '',
            },
            {
                'nombre': 'Risotto de champiñones',
                'descripcion': 'Arroz arbóreo cremoso cocinado con variedad de champiñones salteados y queso parmesano.',
                'categoria': Plato.Categoria.PLATO_FONDO,
                'precio': 10900,
                'stock': 8,
                'tiempo_preparacion': 28,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Puré rústico al merkén',
                'descripcion': 'Puré cremoso de papas nativas con mantequilla y un suave toque de merkén ahumado.',
                'categoria': Plato.Categoria.ACOMPANAMIENTO,
                'precio': 3900,
                'stock': 20,
                'tiempo_preparacion': 12,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Ensalada chilena',
                'descripcion': 'Tomates frescos pelados en gajos con cebolla morada amortiguada, cilantro y aceite de oliva.',
                'categoria': Plato.Categoria.ACOMPANAMIENTO,
                'precio': 3400,
                'stock': 18,
                'tiempo_preparacion': 8,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Leche asada',
                'descripcion': 'Postre casero horneado a base de leche, huevos y vainilla con caramelo artesanal.',
                'categoria': Plato.Categoria.POSTRE,
                'precio': 3800,
                'stock': 16,
                'tiempo_preparacion': 10,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Tiramisú de la casa',
                'descripcion': 'Capas de bizcocho remojado en café espresso, crema mascarpone y cacao amargo.',
                'categoria': Plato.Categoria.POSTRE,
                'precio': 4600,
                'stock': 9,
                'tiempo_preparacion': 10,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
            {
                'nombre': 'Mote con huesillo',
                'descripcion': 'Bebida tradicional chilena bien fría con trigo mote, duraznos deshidratados y jugo acaramelado.',
                'categoria': Plato.Categoria.BEBIDA,
                'precio': 2900,
                'stock': 24,
                'tiempo_preparacion': 5,
                'es_vegetariano': True,
                'disponible': True,
                'imagen_url': '',
            },
        ]

        creados = 0
        for datos in platos_ejemplo:
            # get_or_create evita duplicados si el comando se ejecuta repetidas veces
            _, creado = Plato.objects.get_or_create(
                nombre=datos['nombre'],
                defaults=datos,
            )
            if creado:
                creados += 1

        self.stdout.write(
            self.style.SUCCESS(f'Seed completado: {creados} platos nuevos creados.')
        )
