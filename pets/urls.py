from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list_view, name='pet-list'),
    path('pets/cadastrar/', views.create_pet_view, name='pet-create'),
    path('pets/<int:pk>/', views.pet_detail_view, name='pet-detail'),
    path('pets/<int:pk>/editar/', views.pet_update_view, name='pet-update'),
    path('pets/<int:pk>/deletar/', views.pet_delete_view, name='pet-delete'),
    path('pets/<int:pk>/solicitar/', views.request_adoption_view, name='pet-request'),
    
    path('pedidos/<int:pk>/aprovar/', views.approve_request_view, name='request-approve'),
    path('pedidos/<int:pk>/recusar/', views.decline_request_view, name='request-decline'),
]