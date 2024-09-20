from django.contrib import admin
from products.models import (Category, Product, ProductImagesDesktop,
                             Subcategory)


class SubcategoryInLine(admin.StackedInline):
    model = Subcategory
    extra = 0
    fk_name = 'category'


class ProductInLine(admin.StackedInline):
    model = Product
    extra = 0
    fk_name = 'subcategory'


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        SubcategoryInLine,
    )
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class SubcategoryAdmin(admin.ModelAdmin):
    inlines = (
        ProductInLine,
    )
    list_display = ('name', 'slug', 'category')
    search_fields = ('name', 'slug')
    list_filter = ('category',)


class ProductImagesDesktopInLine(admin.StackedInline):
    model = ProductImagesDesktop
    extra = 0


class ProductImagesDesktopAdmin(admin.ModelAdmin):
    list_display = ('image_detail', 'image_list', 'image_thumbnail')


class ProductAdmin(admin.ModelAdmin):
    inlines = (
        ProductImagesDesktopInLine,
    )
    list_display = ('name', 'slug', 'subcategory')
    search_fields = ('name', 'slug')
    list_filter = ('subcategory',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImagesDesktop, ProductImagesDesktopAdmin)
