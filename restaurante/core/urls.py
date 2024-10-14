# core/urls.py
from django.urls import path
from . import views
from .views import listar_mesas, criar_mesa, atualizar_mesa, deletar_mesa
from django.urls import path
from .views import (
    gerar_relatorio_reservas,
    gerar_relatorio_clientes,
    gerar_relatorio_usuarios,
    gerar_relatorio_mesas,)

from .views import editar_usuario, perfil_usuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),

    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/criar/', views.criar_reserva, name='criar_reserva'),
    path('reservas/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/deletar/<int:pk>/', views.deletar_reserva, name='deletar_reserva'),

    path('menu/', views.menu, name='menu'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name = "registration/logged_out.html"), name='logout'),
    

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
     path('usuarios/<int:user_id>/editar/', editar_usuario, name='editar_usuario'),  # Passa user_id na URL
    path('usuarios/<int:user_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),  # URL para o perfil do usuário

    path('mesas/', listar_mesas, name='listar_mesas'),
    path('mesas/criar/', criar_mesa, name='criar_mesa'),
    path('mesas/atualizar/<int:pk>/', atualizar_mesa, name='atualizar_mesa'),
    path('mesas/deletar/<int:pk>/', deletar_mesa, name='deletar_mesa'),

    path('relatorio/reservas/', gerar_relatorio_reservas, name='gerar_relatorio_reservas'),
    path('relatorio/clientes/', gerar_relatorio_clientes, name='gerar_relatorio_clientes'),
    path('relatorio/usuarios/', gerar_relatorio_usuarios, name='gerar_relatorio_usuarios'),
    path('relatorio/mesas/', gerar_relatorio_mesas, name='gerar_relatorio_mesas'),

]
