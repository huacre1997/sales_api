from django.contrib import admin
from apps.warehouse.models import ProductCategory, Product, UnitMeasure, UnitMeasureCategory, Currency

# Registrando modelos en django admin
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(UnitMeasure)
admin.site.register(UnitMeasureCategory)
admin.site.register(Currency)
