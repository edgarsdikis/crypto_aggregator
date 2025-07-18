# Generated by Django 5.1.7 on 2025-05-31 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0002_alter_token_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolanaTokenDecimals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decimals', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.OneToOneField(limit_choices_to={'chain': 'solana'}, on_delete=django.db.models.deletion.CASCADE, to='tokens.token')),
            ],
        ),
    ]
