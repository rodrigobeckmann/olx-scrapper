from django.contrib import admin
from .models import (
    ScrapedData,
    Product,
    SearchTerm,
    ScrapLog,
)

class SearchTermInline(admin.TabularInline):
    model = SearchTerm
    extra = 1
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

@admin.register(ScrapLog)
class ScrapLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'new_data_scraped', 'pages_scraped', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('id',)
    ordering = ('-created_at',)
