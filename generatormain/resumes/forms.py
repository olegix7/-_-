from django import forms
from django.forms import inlineformset_factory
from .models import Resume, Section, SectionEntry, ResumeTemplate


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'template', 'status',
            'full_name', 'desired_position', 'email', 'phone',
            'address', 'website', 'linkedin', 'summary', 'photo',
        ]
        labels = {
            'title': 'Назва резюме',
            'template': 'Шаблон',
            'status': 'Статус',
            'full_name': 'Повне ім\'я',
            'desired_position': 'Бажана посада',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адреса',
            'website': 'Веб-сайт',
            'linkedin': 'LinkedIn',
            'summary': 'Про себе',
            'photo': 'Фото',
        }
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['template'].queryset = ResumeTemplate.objects.filter(is_active=True)
        self.fields['template'].empty_label = '— Без шаблону —'
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_type', 'title', 'order']
        labels = {
            'section_type': 'Тип секції',
            'title': 'Заголовок',
            'order': 'Порядок',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['order'].widget.attrs.update({'class': 'form-control', 'style': 'width:80px'})


class SectionEntryForm(forms.ModelForm):
    class Meta:
        model = SectionEntry
        fields = ['subtitle', 'date_start', 'date_end', 'location', 'description', 'order']
        labels = {
            'subtitle': 'Підзаголовок (посада, назва, навичка…)',
            'date_start': 'Початок (напр. 2020)',
            'date_end': 'Кінець (напр. 2023 або "Тепер")',
            'location': 'Місце / Організація',
            'description': 'Опис',
            'order': 'Порядок',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


SectionEntryFormSet = inlineformset_factory(
    Section,
    SectionEntry,
    form=SectionEntryForm,
    extra=1,
    can_delete=True,
)
