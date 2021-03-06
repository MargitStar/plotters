from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import UserManager, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if len(User.objects.all()):
            return
        admin = User.objects.create_superuser(username='admin', password='admin')
        admin.save()
