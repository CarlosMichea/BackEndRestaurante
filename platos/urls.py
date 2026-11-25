from django.urls import path
from . import views

# Namespace de la app para referenciar rutas como 'platos:lista', 'platos:crear', etc.
app_name = 'platos'

urlpatterns = [
    path('', views.index, name='index'),
    path('platos/', views.plato_list, name='lista'),
    path('platos/nuevo/', views.plato_create, name='crear'),
    path('platos/<int:pk>/', views.plato_detail, name='detalle'),
    path('platos/<int:pk>/editar/', views.plato_update, name='editar'),
    path('platos/<int:pk>/eliminar/', views.plato_delete, name='eliminar'),
]
