from django.contrib import admin
from .models import ResumeTemplate, Resume, Section, SectionEntry


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'css_class', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)


class SectionEntryInline(admin.TabularInline):
    model = SectionEntry
    extra = 1
    fields = ('subtitle', 'date_start', 'date_end', 'location', 'description', 'order')


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0
    show_change_link = True


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'template', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'template')
    search_fields = ('title', 'owner__username', 'full_name')
    inlines = [SectionInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основне', {'fields': ('owner', 'title', 'template', 'status')}),
        ('Особиста інформація', {'fields': (
            'full_name', 'desired_position', 'email', 'phone',
            'address', 'website', 'linkedin', 'summary', 'photo'
        )}),
        ('Мета', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'resume', 'order')
    list_filter = ('section_type',)
    inlines = [SectionEntryInline]


@admin.register(SectionEntry)
class SectionEntryAdmin(admin.ModelAdmin):
    list_display = ('subtitle', 'section', 'date_start', 'date_end', 'location')
