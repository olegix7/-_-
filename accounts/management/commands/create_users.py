"""
Management command: create_users
Creates a default admin and a default regular user for development/demo.

Admin  : username=admin,  password=Admin1234!,  is_staff=True, role=admin
User   : username=user,   password=User1234!,   role=user
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


USERS = [
    {
        "username": "admin",
        "password": "Admin1234!",
        "first_name": "Адмін",
        "last_name": "Системи",
        "email": "admin@example.com",
        "is_staff": True,
        "is_superuser": True,
        "role": Profile.ROLE_ADMIN,
    },
    {
        "username": "user",
        "password": "User1234!",
        "first_name": "Тест",
        "last_name": "Користувач",
        "email": "user@example.com",
        "is_staff": False,
        "is_superuser": False,
        "role": Profile.ROLE_USER,
    },
]


class Command(BaseCommand):
    help = "Create default admin and regular user accounts for demo/development"

    def handle(self, *args, **options):
        for data in USERS:
            user, created = User.objects.get_or_create(username=data["username"])
            user.set_password(data["password"])
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.is_staff = data["is_staff"]
            user.is_superuser = data["is_superuser"]
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = data["role"]
            profile.save()

            action = "створено" if created else "оновлено"
            self.stdout.write(
                self.style.SUCCESS(
                    f"[{action}] {data['username']} / {data['password']}  (роль: {data['role']})"
                )
            )

        self.stdout.write(self.style.SUCCESS("\nГотово! Облікові записи активні."))
