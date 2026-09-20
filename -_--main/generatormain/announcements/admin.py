from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'author', 'is_published', 'created_at')
    list_filter = ('announcement_type', 'is_published')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Зміст', {'fields': ('announcement_type', 'title', 'content', 'image')}),
        ('Публікація', {'fields': ('author', 'is_published')}),
        ('Мета', {'fields': ('created_at', 'updated_at')}),
    )
