from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages
from pprint import pprint


class ListaProduto(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 9


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # TODO: remover este if
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()
        referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')
        quantidade_solicitada = int(self.request.GET.get('quantidade'))
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = quantidade_solicitada
        slug = produto.slug
        imagem = produto.imagem.name

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += quantidade_solicitada

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}X'
                    f'no produto produto "{produto_nome}"'
                    f'. Adicionamos {variacao_estoque}X no seu carrinho'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = \
                preco_unitario_promocional * quantidade_carrinho

        else:
            # TODO: variação não existe no carrinho.
            if variacao_estoque < quantidade_solicitada:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_solicitada} '
                    f'no produto "{produto_nome}"'
                    f'. Adicionamos {variacao_estoque} X no seu carrinho'
                )
                quantidade_solicitada = variacao_estoque

            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario * quantidade_solicitada,
                'preco_quantitativo_promocional': preco_unitario_promocional * quantidade_solicitada,
                'quantidade': quantidade_solicitada,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho'
            f' {quantidade_solicitada} X'
        )
        return redirect(referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            return redirect(referer)
        if not self.request.session.get('carrinho'):
            return redirect(referer)
        if variacao_id not in self.request.session['carrinho']:
            return redirect(referer)

        carrinho = self.request.session['carrinho']

        messages.success(
            self.request,
            f'Produto >> {carrinho[variacao_id]["produto_nome"]} {carrinho[variacao_id]["variacao_nome"]} <<'
            f' removido do seu carrinho'
        )
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho')
        }
        return render(self.request, 'produto/carrinho.html', contexto)


class ResumodaCompra(View):
    def get(*args, **kwargs):
        return HttpResponse('Finalizar')
