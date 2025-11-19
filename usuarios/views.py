from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from pets.models import AdoptionRequest

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pet-list')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'usuarios/register.html', context)

@login_required
def dashboard_view(request):
    pedidos_recebidos = AdoptionRequest.objects.filter(
        pet__dono=request.user
    ).order_by('-data_solicitacao')
    
    context = {
        'pedidos': pedidos_recebidos
    }
    return render(request, 'usuarios/dashboard.html', context)
@login_required
def my_adoptions_view(request):
    meus_pedidos = AdoptionRequest.objects.filter(
        solicitante=request.user
    ).order_by('-data_solicitacao')
    
    context = {
        'pedidos': meus_pedidos
    }
    return render(request, 'usuarios/my_adoptions.html', context)