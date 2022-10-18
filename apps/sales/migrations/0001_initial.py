# Generated by Django 4.1.2 on 2022-10-18 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        ('warehouse', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('address', models.CharField(max_length=100, verbose_name='Dirección')),
                ('date', models.DateField(verbose_name='Fecha de entrega')),
                ('status', models.BooleanField(default=True, verbose_name='Estado de entrega')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('district', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.district', verbose_name='Distrito')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
                'db_table': 'delivery',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('code', models.CharField(max_length=9, unique=True, verbose_name='Número del Pedido')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='Cliente')),
                ('delivery', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sales.delivery', verbose_name='Entrega')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de modificación')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Cantidad')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Monto de Descuento')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Subtotal')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sales.order', verbose_name='Pedido')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='warehouse.product', verbose_name='Producto')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Detalle del Pedido',
                'verbose_name_plural': 'Detalles del Pedido',
                'db_table': 'order_detail',
            },
        ),
    ]
