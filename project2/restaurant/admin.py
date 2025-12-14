from django.contrib import admin
from .models import Category, MenuItem, MenuItemImage, Chef, Review


class MenuItemImageInline(admin.TabularInline):
    model = MenuItemImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "discount_price",
        "is_available",
        "is_featured",
        "views_count",
    ]
    list_filter = [
        "category",
        "is_available",
        "is_featured",
        "is_vegetarian",
        "is_spicy",
    ]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MenuItemImageInline]
    readonly_fields = ["views_count"]


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["name", "position"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "menu_item", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["user__username", "menu_item__name", "comment"]
