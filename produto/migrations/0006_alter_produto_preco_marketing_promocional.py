# Generated by Django 3.2.8 on 2021-10-23 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_auto_20211022_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing_promocional',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Preço Promo'),
        ),
    ]
