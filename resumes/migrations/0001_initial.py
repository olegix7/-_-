from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва шаблону')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('preview_image', models.ImageField(
                    blank=True, null=True,
                    upload_to='templates/',
                    verbose_name='Зображення попереднього перегляду'
                )),
                ('css_class', models.CharField(default='template-classic', max_length=50, verbose_name='CSS клас')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активний')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Шаблон резюме',
                'verbose_name_plural': 'Шаблони резюме',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Назва резюме')),
                ('status', models.CharField(
                    choices=[('draft', 'Чернетка'), ('published', 'Опубліковано')],
                    default='draft', max_length=20, verbose_name='Статус'
                )),
                ('full_name', models.CharField(blank=True, max_length=150, verbose_name="Повне ім'я")),
                ('desired_position', models.CharField(blank=True, max_length=200, verbose_name='Бажана посада')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адреса')),
                ('website', models.URLField(blank=True, verbose_name='Веб-сайт')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn')),
                ('summary', models.TextField(blank=True, verbose_name='Про себе')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='resume_photos/', verbose_name='Фото')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='resumes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Власник'
                )),
                ('template', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='resumes',
                    to='resumes.resumetemplate',
                    verbose_name='Шаблон'
                )),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(
                    choices=[
                        ('experience', 'Досвід роботи'),
                        ('education', 'Освіта'),
                        ('skills', 'Навички'),
                        ('languages', 'Мови'),
                        ('certifications', 'Сертифікати'),
                        ('projects', 'Проекти'),
                        ('custom', 'Власна секція'),
                    ],
                    max_length=20, verbose_name='Тип секції'
                )),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок секції')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('resume', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sections',
                    to='resumes.resume'
                )),
            ],
            options={
                'verbose_name': 'Секція',
                'verbose_name_plural': 'Секції',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SectionEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitle', models.CharField(blank=True, max_length=255, verbose_name='Підзаголовок')),
                ('date_start', models.CharField(blank=True, max_length=50, verbose_name='Початок')),
                ('date_end', models.CharField(blank=True, max_length=50, verbose_name='Кінець')),
                ('location', models.CharField(blank=True, max_length=150, verbose_name='Місце')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('section', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='entries',
                    to='resumes.section'
                )),
            ],
            options={
                'verbose_name': 'Запис секції',
                'verbose_name_plural': 'Записи секцій',
                'ordering': ['order'],
            },
        ),
    ]
