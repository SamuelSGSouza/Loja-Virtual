from django.template import Library
from utils import utils
register = Library()


@register.filter
def formata_preco(val):
    return utils.formatatexto(val)


@register.filter
def soma_quantidades_carrinho(carrinho):
    return utils.soma_quantidades_carr(carrinho)


@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)
