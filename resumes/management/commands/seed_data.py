"""
Management command to populate the database with initial seed data.

Usage:
    python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from resumes.models import ResumeTemplate
from announcements.models import Announcement


TEMPLATES = [
    {
        'name': 'Класичний',
        'description': 'Чистий класичний дизайн у синіх тонах. Підходить для більшості галузей.',
        'css_class': 'template-classic',
    },
    {
        'name': 'Сучасний',
        'description': 'Свіжий зелений акцент. Ідеальний для IT та стартапів.',
        'css_class': 'template-modern',
    },
    {
        'name': 'Мінімалістичний',
        'description': 'Строгий темний стиль без зайвих елементів. Для топ-менеджменту.',
        'css_class': 'template-minimal',
    },
    {
        'name': 'Креативний',
        'description': 'Яскравий фіолетовий акцент. Для дизайнерів та творчих спеціальностей.',
        'css_class': 'template-creative',
    },
    {
        'name': 'Елегантний',
        'description': 'Рожево-малиновий стиль. Вишуканий та привабливий вигляд.',
        'css_class': 'template-elegant',
    },
    {
        'name': 'Корпоративний',
        'description': 'Теплий золотисто-коричневий дизайн. Для фінансів та бізнесу.',
        'css_class': 'template-corporate',
    },
]

ANNOUNCEMENTS = [
    {
        'type': 'news',
        'title': 'Вітаємо на платформі Резюме-білдер!',
        'content': (
            'Ми раді вітати вас на нашій платформі для створення професійних резюме.\n\n'
            'Тут ви можете:\n'
            '• Обрати красивий шаблон\n'
            '• Заповнити свої дані\n'
            '• Додати досвід роботи, освіту та навички\n'
            '• Завантажити готове резюме у форматах PDF або DOCX\n\n'
            'Бажаємо успіху у пошуку роботи!'
        ),
    },
    {
        'type': 'announcement',
        'title': 'Нові шаблони резюме вже доступні',
        'content': (
            'Додано 6 нових шаблонів резюме на вибір:\n\n'
            '• Класичний — для будь-якої галузі\n'
            '• Сучасний — для IT та технологій\n'
            '• Мінімалістичний — суворий та діловий\n'
            '• Креативний — для творчих спеціальностей\n'
            '• Елегантний — вишуканий стиль\n'
            '• Корпоративний — для бізнесу та фінансів\n\n'
            'Переходьте до каталогу шаблонів та обирайте!'
        ),
    },
    {
        'type': 'news',
        'title': 'Поради щодо створення успішного резюме',
        'content': (
            'Кілька порад для створення резюме, яке привертає увагу:\n\n'
            '1. Адаптуйте резюме під кожну вакансію — використовуйте функцію клонування\n'
            '2. Вказуйте конкретні досягнення з цифрами\n'
            '3. Не перевантажуйте резюме — тримайтесь 1-2 сторінок\n'
            '4. Перевіряйте граматику та орфографію\n'
            '5. Додайте фото — це підвищує довіру\n\n'
            'Удачі у пошуку роботи!'
        ),
    },
]


class Command(BaseCommand):
    help = 'Заповнює базу даних початковими даними (шаблони, оголошення)'

    def handle(self, *args, **options):
        self.stdout.write('Починаємо заповнення бази даних...\n')

        # ── Templates ────────────────────────────────────────────
        created_count = 0
        for tmpl_data in TEMPLATES:
            obj, created = ResumeTemplate.objects.get_or_create(
                name=tmpl_data['name'],
                defaults={
                    'description': tmpl_data['description'],
                    'css_class': tmpl_data['css_class'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Шаблон: {obj.name}')
            else:
                self.stdout.write(f'  — Шаблон вже існує: {obj.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nШаблони: {created_count} створено, {len(TEMPLATES) - created_count} вже існували.'
        ))

        # ── Announcements (need an author — first superuser or skip) ──
        author = User.objects.filter(is_superuser=True).first()

        ann_created = 0
        for ann_data in ANNOUNCEMENTS:
            obj, created = Announcement.objects.get_or_create(
                title=ann_data['title'],
                defaults={
                    'announcement_type': ann_data['type'],
                    'content': ann_data['content'],
                    'author': author,
                    'is_published': True,
                }
            )
            if created:
                ann_created += 1
                self.stdout.write(f'  ✓ Оголошення: {obj.title}')
            else:
                self.stdout.write(f'  — Оголошення вже існує: {obj.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nОголошення: {ann_created} створено, {len(ANNOUNCEMENTS) - ann_created} вже існували.'
        ))

        # ── Demo user (optional, only in DEBUG) ──────────────────
        from django.conf import settings
        if settings.DEBUG and not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user(
                username='demo',
                password='demo1234',
                first_name='Демо',
                last_name='Користувач',
                email='demo@example.com',
            )
            Profile.objects.get_or_create(user=demo)
            self.stdout.write(self.style.SUCCESS(
                '\n  ✓ Демо-користувач створено: demo / demo1234'
            ))

        self.stdout.write(self.style.SUCCESS('\n✅ База даних успішно заповнена!\n'))
