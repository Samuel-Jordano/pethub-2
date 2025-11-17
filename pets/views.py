from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet, AdoptionRequest
from .forms import PetForm

def pet_list_view(request):
    pets = Pet.objects.filter(status_adocao='disponivel')
    context = {
        'pets': pets
    }
    return render(request, 'pets/pet_list.html', context)

@login_required
def create_pet_view(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.dono = request.user
            pet.save()
            return redirect('pet-list')
    else:
        form = PetForm()
    
    context = {'form': form}
    return render(request, 'pets/pet_form.html', context)

def pet_detail_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    context = {
        'pet': pet
    }
    return render(request, 'pets/pet_detail.html', context)

@login_required
def pet_update_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.user != pet.dono:
        return redirect('pet-list')
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet-detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    context = {'form': form, 'pet': pet}
    return render(request, 'pets/pet_form.html', context)

@login_required
def pet_delete_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.user != pet.dono:
        return redirect('pet-list')
    if request.method == 'POST':
        pet.delete()
        return redirect('pet-list')
    context = {'pet': pet}
    return render(request, 'pets/pet_delete_confirm.html', context)

@login_required
def request_adoption_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    
    if request.method == 'POST':
        if pet.dono != request.user and pet.status_adocao == 'disponivel':
            
            existing_request = AdoptionRequest.objects.filter(
                pet=pet, 
                solicitante=request.user
            ).exists()
            
            if not existing_request:
                AdoptionRequest.objects.create(pet=pet, solicitante=request.user)

    return redirect('pet-detail', pk=pet.pk)

@login_required
def approve_request_view(request, pk):
    pedido = get_object_or_404(AdoptionRequest, pk=pk)

    if request.user != pedido.pet.dono:
        return redirect('dashboard')

    if request.method == 'POST':
        pedido.status = 'aprovado'
        pedido.save()
        
        pet = pedido.pet
        pet.status_adocao = 'adotado'
        pet.save()
        
        AdoptionRequest.objects.filter(pet=pet, status='pendente').update(status='recusado')

    return redirect('dashboard')

@login_required
def decline_request_view(request, pk):
    pedido = get_object_or_404(AdoptionRequest, pk=pk)

    if request.user != pedido.pet.dono:
        return redirect('dashboard')

    if request.method == 'POST':
        pedido.status = 'recusado'
        pedido.save()

    return redirect('dashboard')