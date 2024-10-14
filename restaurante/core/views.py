
# core/views.py
from .models import Cliente, Mesa, Reserva
from .forms import ClienteForm, ReservaForm, MesaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import EditUserForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# menu
@login_required
def menu(request):
    return render(request, 'menu.html')

# cliente
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/clientes/lista_clientes.html', {'clientes': clientes})

@login_required
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'core/clientes/criar_cliente.html', {'form': form})
# reservas
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reservas/lista_reservas.html', {'reservas': reservas})

@login_required
def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'core/reservas/criar_reserva.html', {'form': form})

@login_required
def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    mesas = Mesa.objects.all()  # Obtém todas as mesas

    if request.method == 'POST':
        reserva.data_reserva = request.POST['data_reserva']
        reserva.hora_reserva = request.POST['hora_reserva']
        reserva.num_pessoas = request.POST['num_pessoas']
        reserva.mesa_id = request.POST['mesa']  # Supondo que você tenha uma relação de ForeignKey

        reserva.save()
        return redirect('lista_reservas')  # Redireciona para a lista de reservas

    return render(request, 'core/reservas/editar_reserva.html', {'reserva': reserva, 'mesas': mesas})

@login_required
def deletar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        reserva.delete()
        return redirect('listar_reservas')  # Redireciona para a lista de reservas

    return render(request, 'core/reservas/deletar_reserva.html', {'reserva': reserva})

# Tudo sobre usuário
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/usuarios/listar_usuarios.html', {'usuarios': usuarios})



@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # Redireciona para uma página de sucesso
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/usuarios/criar_usuario.html', {'form': form})

@login_required
def editar_usuario(request, user_id):  # Adicione user_id como argumento
    user = get_object_or_404(User, id=user_id)  # Obtenha o usuário com base no ID

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Salva as alterações
            return redirect('perfil_usuario')  # Redireciona para uma página após a edição
    else:
        form = EditUserForm(instance=user)

    return render(request, 'core/usuarios/editar_usuario.html', {'form': form})

@login_required
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html')  # Substitua pelo seu template

@login_required
def deletar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'core/usuarios/deletar_usuario.html', {'usuario': usuario})


# View para listar mesas
@login_required
def listar_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'core/mesas/listar_mesas.html', {'mesas': mesas})

# View para criar mesa
@login_required
def criar_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm()
    return render(request, 'core/mesas/criar_mesa.html', {'form': form})

# View para atualizar mesa
@login_required
def atualizar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'core/mesas/criar_mesa.html', {'form': form, 'mesa': mesa})

# View para deletar mesa
@login_required
def deletar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('listar_mesas')
    return render(request, 'core/mesas/deletar_mesa.html', {'mesa': mesa})


# Função genérica para gerar PDF
def gerar_pdf(html_string, nome_arquivo):
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={nome_arquivo}.pdf'
    return response

# Gerar PDF de Reservas
@login_required
def gerar_relatorio_reservas(request):
    reservas = Reserva.objects.all()
    html_string = render_to_string('core/relatorio_reservas.html', {'reservas': reservas})
    
    return gerar_pdf(html_string, 'relatorio_reservas')

# Gerar PDF de Clientes
@login_required
def gerar_relatorio_clientes(request):
    clientes = Cliente.objects.all()
    
    html_string = render_to_string('core/relatorio_clientes.html', {'clientes': clientes})
    return gerar_pdf(html_string, 'relatorio_clientes')

# Gerar PDF de Usuários
@login_required
def gerar_relatorio_usuarios(request):
    usuarios = User.objects.all()
    html_string = render_to_string('core/relatorio_usuarios.html', {'usuarios': usuarios})
    return gerar_pdf(html_string, 'relatorio_usuarios')

# Gerar PDF de Mesas
@login_required
def gerar_relatorio_mesas(request):
    mesas = Mesa.objects.all()
    html_string = render_to_string('core/relatorio_mesas.html', {'mesas': mesas})
    return gerar_pdf(html_string, 'relatorio_mesas')




