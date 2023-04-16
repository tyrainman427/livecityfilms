from django.contrib import admin
from .models import *

class PriceInlineAdmin(admin.TabularInline):
    model = OrderDetail
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]


admin.site.register(Product, ProductAdmin)

# Register your models here.
admin.site.register(Contact)
admin.site.register(OrderDetail)