from django.urls import path
from .import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProduto.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/',
         views.AdicionarAoCarrinho.as_view(), name='adicionar'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='remover'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumodaCompra.as_view(), name='resumo'),
]
