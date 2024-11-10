from django.contrib import admin
from .models import ScrapedData, Product, SearchTerm

class SearchTermInline(admin.TabularInline):  # Ou admin.StackedInline para um layout diferente
    model = SearchTerm
    extra = 1  # Número de linhas extras vazias para adicionar novas instâncias
    fields = ('term',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'olx_id', 'title', 'url', 'archived', 'created_at', 'updated_at')
    list_filter = ('archived', 'created_at', 'updated_at')
    search_fields = ('olx_id', 'title')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('olx_id', 'title', 'description', 'url', 'img_url', 'archived')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SearchTermInline]
