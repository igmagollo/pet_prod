from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# NAO ESQUEÇAM DE ATUALIZAR OS IMPORTS
from .models import Medico, Rodada
from .forms import Medico_Form, Rodada_Form

# from django.core.exceptions import ObjectDoesNotExist

# views para home

@login_required(login_url='/login/')
def index(request):
    return render(request, 'jogo/index.html', {})


def base_configuracoes(request):
    return render(request, 'jogo/base_configuracoes.html', {})


def base_aplicar_dinamica(request):
    return render(request, 'jogo/base_aplicar_dinamica.html', {})


def login(request):
    contexto = {}
    if request.method == 'POST':
        try:
            usuario = request.POST['usuario']
            senha = request.POST['senha']

            try:
                user = User.objects.get(username=usuario)

                if user.is_active:
                    usuario_autenticado = authenticate(username=usuario, password=senha)

                    if usuario_autenticado is not None:
                        django_login(request, usuario_autenticado)
                        return HttpResponseRedirect('/home/')
                    else:
                        contexto['erro'] = 'Usuário ou senha inválidos.'
                else:
                    contexto['erro'] = 'Usuário inativo.'
            except:
                contexto['erro'] = 'Usuário inexistente.'
        except:
            contexto['erro'] = 'Parâmetros inválidos.'

    return render(request, 'jogo/login.html', contexto)


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)

    return HttpResponseRedirect('/login/')



# Views para médico:

def medico_index(request):
    medicos = Medico.objects.order_by('perfil')
    return render(request, 'medico/medico_index.html', {'medicos':medicos})

# TODO login_required
#@login_required(login_url='/adm/login/')
def medico_new(request):
    medico = None
    try:
        medico = Medico.objects.latest('id')
    except:
        pass
    if medico == None:
        id = 1
    else:
        id = medico.id + 1

    if request.method == 'POST':
        form = Medico_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')
        else:
            return render(request, 'medico/medico_new.html', {'form':form, 'id':id})
    else:
        form = Medico_Form()
        return render(request, 'medico/medico_new.html', {'form': form, 'id':id})

# TODO login_required
#@login_required(login_url='/adm/login/')
def medico_edit(request, id):
    medico = get_object_or_404(Medico,pk=id)
    form = Medico_Form(instance=medico)

    if request.method == 'POST':
        form = Medico_Form(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')

    return render(request, 'medico/medico_edit.html', {'form':form, 'id':id})

# TODO login_required
#@login_required(login_url='/adm/login/')
def medico_delete(request, id):
    get_object_or_404(Medico, pk=id).delete()
    return HttpResponseRedirect('/medico')

def rodada_index(request):
    rodadas = Rodada.objects.order_by('numeroRodada')
    return render(request, 'rodada/rodada_index.html', {'rodadas':rodadas})

# TODO login_required
#@login_required(login_url='/adm/login/')
def rodada_new(request):
    # TODO verificar se esta parte deve ser descomentada
    # rodada = None
    # try:
    #     rodada = Rodada.objects.latest('numeroRodada')
    # except:
    #     pass
    # if rodada == None:
    #     numeroRodada = 1
    # else:
    #     numeroRodada = rodada.numeroRodada + 1

    if request.method == 'POST':
        form = Rodada_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')
        else:
            return render(request, 'rodada/rodada_new.html', {'form':form})
    else:
        form = Rodada_Form()
        return render(request, 'rodada/rodada_new.html', {'form': form})

# TODO login_required
#@login_required(login_url='/adm/login/')
def rodada_edit(request, id):
    rodada = get_object_or_404(Rodada,pk=id)
    form = Rodada_Form(instance=rodada)

    if request.method == 'POST':
        form = Rodada_Form(request.POST, instance=rodada)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')

    return render(request, 'rodada/rodada_edit.html', {'form':form})