from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.bienvenida, name='bienvenida'),
    path('api/usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('api/usuarios/<int:usuario_id>/', views.usuarios_detalle, name='usuarios_detalle'),
]