import json
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from shop.models import Category, Product, ProductImage, ShopSettings


class Command(BaseCommand):
    help = 'Load the starting products and photos from seed/data.json.'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing products first.')

    def handle(self, *args, **opts):
        seed = Path(settings.BASE_DIR) / 'seed'
        data = json.loads((seed / 'data.json').read_text(encoding='utf-8'))
        if Product.objects.exists():
            if not opts['reset']:
                raise CommandError('Products already exist. Use --reset to replace them.')
            Product.objects.all().delete()
            Category.objects.all().delete()

        s = data['settings']
        shop = ShopSettings.load()
        shop.shop_name, shop.tagline, shop.phone = s['shopName'], s['tagline'], s['phone']
        shop.whatsapp, shop.location, shop.hours = s['whatsapp'], s['location'], s['hours']
        shop.save()

        cats = {}
        for i, p in enumerate(data['products']):
            if p['category'] not in cats:
                cats[p['category']], _ = Category.objects.get_or_create(name=p['category'], defaults={'order': len(cats)})
            prod = Product.objects.create(
                name=p['name'], category=cats[p['category']], price=p['price'], price_max=p.get('priceMax') or 0,
                description=p.get('description', ''), in_stock=p.get('inStock', True), order=i)
            for j, img in enumerate(p.get('images', [])):
                with open(seed / img, 'rb') as fh:
                    ProductImage.objects.create(product=prod, image=File(fh, name=img), order=j)
        self.stdout.write(self.style.SUCCESS(f'Imported {Product.objects.count()} products.'))
