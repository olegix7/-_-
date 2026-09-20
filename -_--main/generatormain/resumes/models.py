from django.db import models
from django.contrib.auth.models import User


class ResumeTemplate(models.Model):
    """Pre-defined visual templates for resumes."""
    name = models.CharField(max_length=100, verbose_name='Назва шаблону')
    description = models.TextField(blank=True, verbose_name='Опис')
    preview_image = models.ImageField(
        upload_to='templates/', blank=True, null=True, verbose_name='Зображення попереднього перегляду'
    )
    css_class = models.CharField(
        max_length=50, default='template-classic', verbose_name='CSS клас'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Шаблон резюме'
        verbose_name_plural = 'Шаблони резюме'
        ordering = ['name']

    def __str__(self):
        return self.name


class Resume(models.Model):
    """Main resume model."""
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Чернетка'),
        (STATUS_PUBLISHED, 'Опубліковано'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', verbose_name='Власник')
    template = models.ForeignKey(
        ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resumes', verbose_name='Шаблон'
    )
    title = models.CharField(max_length=200, verbose_name='Назва резюме')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, verbose_name='Статус')

    # Personal info
    full_name = models.CharField(max_length=150, blank=True, verbose_name='Повне ім\'я')
    desired_position = models.CharField(max_length=200, blank=True, verbose_name='Бажана посада')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адреса')
    website = models.URLField(blank=True, verbose_name='Веб-сайт')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    summary = models.TextField(blank=True, verbose_name='Про себе')
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True, verbose_name='Фото')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.title} ({self.owner.username})'

    def clone(self):
        """Create a copy of this resume with all its sections."""
        new_resume = Resume.objects.create(
            owner=self.owner,
            template=self.template,
            title=f'Копія — {self.title}',
            status=self.STATUS_DRAFT,
            full_name=self.full_name,
            desired_position=self.desired_position,
            email=self.email,
            phone=self.phone,
            address=self.address,
            website=self.website,
            linkedin=self.linkedin,
            summary=self.summary,
        )
        for section in self.sections.all():
            section.clone_to(new_resume)
        return new_resume


class Section(models.Model):
    """A section within a resume (experience, education, skills, etc.)."""
    TYPE_EXPERIENCE = 'experience'
    TYPE_EDUCATION = 'education'
    TYPE_SKILLS = 'skills'
    TYPE_LANGUAGES = 'languages'
    TYPE_CERTIFICATIONS = 'certifications'
    TYPE_PROJECTS = 'projects'
    TYPE_CUSTOM = 'custom'

    TYPE_CHOICES = [
        (TYPE_EXPERIENCE, 'Досвід роботи'),
        (TYPE_EDUCATION, 'Освіта'),
        (TYPE_SKILLS, 'Навички'),
        (TYPE_LANGUAGES, 'Мови'),
        (TYPE_CERTIFICATIONS, 'Сертифікати'),
        (TYPE_PROJECTS, 'Проекти'),
        (TYPE_CUSTOM, 'Власна секція'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип секції')
    title = models.CharField(max_length=150, verbose_name='Заголовок секції')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Секція'
        verbose_name_plural = 'Секції'
        ordering = ['order']

    def __str__(self):
        return f'{self.get_section_type_display()} — {self.resume.title}'

    def clone_to(self, target_resume):
        new_section = Section.objects.create(
            resume=target_resume,
            section_type=self.section_type,
            title=self.title,
            order=self.order,
        )
        for entry in self.entries.all():
            SectionEntry.objects.create(
                section=new_section,
                subtitle=entry.subtitle,
                date_start=entry.date_start,
                date_end=entry.date_end,
                location=entry.location,
                description=entry.description,
                order=entry.order,
            )
        return new_section


class SectionEntry(models.Model):
    """A single entry inside a section (one job, one degree, one skill, etc.)."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='entries')
    subtitle = models.CharField(max_length=255, blank=True, verbose_name='Підзаголовок')
    date_start = models.CharField(max_length=50, blank=True, verbose_name='Початок')
    date_end = models.CharField(max_length=50, blank=True, verbose_name='Кінець')
    location = models.CharField(max_length=150, blank=True, verbose_name='Місце')
    description = models.TextField(blank=True, verbose_name='Опис')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Запис секції'
        verbose_name_plural = 'Записи секцій'
        ordering = ['order']

    def __str__(self):
        return f'{self.subtitle} ({self.section})'
