"""
Management command to create a default superuser non-interactively.

Usage:
    python manage.py create_admin
    python manage.py create_admin --username admin --password admin123 --email admin@example.com
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Створює суперкористувача без інтерактивного введення'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin',    help='Логін (default: admin)')
        parser.add_argument('--password', default='admin123', help='Пароль  (default: admin123)')
        parser.add_argument('--email',    default='admin@example.com', help='Email')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email    = options['email']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Користувач "{username}" вже існує. Оновлюємо пароль...'
            ))
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff     = True
            user.is_superuser = True
            user.save()
        else:
            user = User.objects.create_superuser(
                username=username,
                password=password,
                email=email,
                first_name='Адмін',
                last_name='',
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Суперкористувач "{username}" створено.'))

        # Ensure profile with admin role exists
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = Profile.ROLE_ADMIN
        profile.save()

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Готово!\n'
            f'   Логін:  {username}\n'
            f'   Пароль: {password}\n'
            f'   URL:    http://127.0.0.1:8000/admin/\n'
        ))
