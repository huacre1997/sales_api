from django.contrib import admin

from apps.crm.models import Customer, District, CustomerCategory

# REgistrando modelos en django admin
admin.site.register(Customer)
admin.site.register(District)
admin.site.register(CustomerCategory)
