from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models


class Pagar(ListView):
    template_name = 'pedido/index.html'
    model = models.Pedido


class SalvarPedido(View):
    def get(*args, **kwargs):
        return HttpResponse('FecharPedido')


class Detalhe(View):
    def get(*args, **kwargs):
        return HttpResponse('Detalhe')


# Create your views here.
