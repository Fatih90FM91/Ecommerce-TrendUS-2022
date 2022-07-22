from django.contrib import admin

from . models import *



# Register your models here.

class PostImageAdmin(admin.StackedInline):
    model = PostImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = Product

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer)
#admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
