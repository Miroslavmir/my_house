from django.contrib import admin
from goods import models


@admin.register(models.Categories)
class CategoriesModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name",)


@admin.register(models.Products)
class ProductsModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "quantity", "price", "discount")
    list_editable = ("discount",)
    search_fields = ("name", "description")
    list_filter = ("discount", "quantity", "category")
    fields = (
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    )