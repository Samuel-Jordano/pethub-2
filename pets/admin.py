from django.contrib import admin
from .models import Pet, AdoptionRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'dono', 'status_adocao')
    list_filter = ('status_adocao', 'especie')
    search_fields = ('nome', 'dono__username')

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'solicitante', 'status')
    list_filter = ('status',)
    search_fields = ('pet__nome', 'solicitante__username')