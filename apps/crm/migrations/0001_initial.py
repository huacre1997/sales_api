# Generated by Django 4.1.2 on 2022-10-18 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('name', models.CharField(max_length=40, verbose_name='Nombre del Distrito')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Distrito',
                'verbose_name_plural': 'Distritos',
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='CustomerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre de la categoría del cliente')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Categoria del cliente',
                'verbose_name_plural': 'Categorías del cliente',
                'db_table': 'customer_category',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('company_name', models.CharField(max_length=100, verbose_name='Razón social')),
                ('ruc', models.CharField(max_length=11, unique=True, verbose_name='RUC')),
                ('customer_category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.customercategory', verbose_name='Categoria del Cliente')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('district', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.district', verbose_name='Distrito')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'customer',
            },
        ),
    ]
