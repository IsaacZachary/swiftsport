from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import secrets

MODELS = ['product', 'productimage', 'category', 'shopsettings']


class Command(BaseCommand):
    help = 'Create a staff login that can only manage products, photos, categories and shop details.'

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **opts):
        group, _ = Group.objects.get_or_create(name='Shop managers')
        perms = Permission.objects.filter(content_type__app_label='shop', content_type__model__in=MODELS)
        group.permissions.set(perms.exclude(codename='delete_shopsettings'))
        User = get_user_model()
        user, created = User.objects.get_or_create(username=opts['username'])
        user.is_staff = True
        if created:
            pw = secrets.token_urlsafe(9)
            user.set_password(pw)
        user.save()
        user.groups.add(group)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created {user.username}. Temporary password: {pw}'))
            self.stdout.write('Ask them to change it after logging in (top right: Change password).')
        else:
            self.stdout.write(self.style.SUCCESS(f'{user.username} can now manage the shop.'))
