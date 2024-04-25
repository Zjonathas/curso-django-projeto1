from django.contrib import admin
from .models import Category, Recipe
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag


class TagInLine(GenericStackedInline):
    model = Tag
    fiels = 'name',
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_publish', 'author'
    list_display_links = 'title', 'created_at'
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_publish', \
        'preparation_steps_html'
    list_per_page = 10
    list_editable = 'is_publish',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }

    inlines = [
        TagInLine,
    ]


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
