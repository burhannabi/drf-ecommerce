from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductImage, ProductLine

# Register your models here.


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        else:
            return ""


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class PoductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        PoductLineInline,
    ]


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)

# class ProductLineInline(admin.TabularInline):
#     model = ProductLine


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductLineInline]
