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
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_type', models.CharField(
                    choices=[('news', 'Новина'), ('announcement', 'Оголошення')],
                    default='announcement', max_length=20, verbose_name='Тип'
                )),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Зміст')),
                ('image', models.ImageField(
                    blank=True, null=True,
                    upload_to='announcements/',
                    verbose_name='Зображення'
                )),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубліковано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('author', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='announcements',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор'
                )),
            ],
            options={
                'verbose_name': 'Оголошення',
                'verbose_name_plural': 'Оголошення',
                'ordering': ['-created_at'],
            },
        ),
    ]
