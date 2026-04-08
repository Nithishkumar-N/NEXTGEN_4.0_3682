"""
Management command: create_default_admin
Creates the default PartLink superuser if it does not already exist.

Usage:
    python manage.py create_default_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create the default PartLink admin account."

    # Default credentials (change after first login in production!)
    USERNAME = "admin"
    EMAIL    = "admin@partlink.local"
    PASSWORD = "Admin@1234"

    def handle(self, *args, **kwargs):
        if User.objects.filter(username=self.USERNAME).exists():
            self.stdout.write(self.style.WARNING(
                f'Admin user "{self.USERNAME}" already exists. Skipping creation.'
            ))
        else:
            User.objects.create_superuser(
                username=self.USERNAME,
                email=self.EMAIL,
                password=self.PASSWORD,
            )
            self.stdout.write(self.style.SUCCESS(
                f'\n✅  Default admin created!\n'
                f'   Username : {self.USERNAME}\n'
                f'   Password : {self.PASSWORD}\n'
                f'   Email    : {self.EMAIL}\n'
                f'\n⚠️   Please change the password after first login!\n'
            ))
