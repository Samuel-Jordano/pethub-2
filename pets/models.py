from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    STATUS_CHOICES = (
        ('disponivel', 'Disponível'),
        ('adotado', 'Adotado'),
    )

    ESPECIE_CHOICES = (
        ('cao', 'Cão'),
        ('gato', 'Gato'),
    )
    
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES) # <-- MODIFICADO AQUI
    raca = models.CharField(max_length=50, blank=True, null=True)
    idade = models.PositiveIntegerField()
    descricao = models.TextField(max_length=500)
    foto = models.ImageField(upload_to='pets_fotos/')
    status_adocao = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponivel'
    )

    def __str__(self):
        return self.nome

class AdoptionRequest(models.Model):
    STATUS_PEDIDO_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
    )

    solicitante = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='pedidos_feitos'
    )
    pet = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE, 
        related_name='pedidos'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_PEDIDO_CHOICES, 
        default='pendente'
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.solicitante.username} para {self.pet.nome}"