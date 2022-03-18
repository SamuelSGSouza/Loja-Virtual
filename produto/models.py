from PIL import Image
from django.db import models
from django.db.models.fields import CharField
import os
from django.conf import settings
from django.utils.text import slugify
from utils import utils


class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name='nome_produto')
    descricao_curta = models.TextField(
        max_length=255, verbose_name='Descrição')
    descricao_longa = models.TextField(verbose_name='desc_longa_produto')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name='Preço Promo', null=True, blank=True)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return utils.formatatexto(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promo_formatado(self):
        if self.preco_marketing_promocional:
            return utils.formatatexto(self.preco_marketing_promocional)
        return ''
    get_preco_promo_formatado.short_description = 'Preço Promocional'

    @staticmethod
    def resize_image(img, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_heigth = img_pil.size

        if not original_width <= new_width:
            img_pil.close()
            return

        new_height = round((original_heigth * new_width) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        new_img.save(
            img_full_path,
            quality=50,
            optimize=True

        )
        print('a imagem foi redimensionada')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    nome = models.CharField(max_length=50)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Varições'
