# Generated by Django 5.1.7 on 2025-05-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coingeckoprice',
            name='price_usd',
            field=models.DecimalField(decimal_places=24, max_digits=50),
        ),
        migrations.AlterField(
            model_name='coinmarketcapprice',
            name='price_usd',
            field=models.DecimalField(decimal_places=24, max_digits=50),
        ),
    ]
