from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageOps

MAX_SIDE = 1200


class ShopSettings(models.Model):
    """Shop details shown on the website. There is only ever one row."""
    shop_name = models.CharField(max_length=80, default='Swift Sport')
    tagline = models.CharField(max_length=80, default='Sports & Tactical Gear')
    phone = models.CharField('phone shown on the site', max_length=30, default='0712 984 925')
    whatsapp = models.CharField('WhatsApp number', max_length=15, default='254712984925',
                                help_text='Country code first, no + or spaces, e.g. 254712984925')
    location = models.CharField(max_length=200, default='Airport North Road, Soweto–Baraka, opposite Embakasi Garrison, Embakasi, Nairobi')
    hours = models.CharField('opening hours', max_length=80, default='Open daily, 8am – 8pm')

    class Meta:
        verbose_name = 'shop details'
        verbose_name_plural = 'shop details'

    def __str__(self):
        return 'Shop details'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers show first.')

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    price = models.PositiveIntegerField('price (KES)', default=0, help_text='0 shows "Ask for price".')
    price_max = models.PositiveIntegerField('highest price (KES)', default=0, blank=True,
                                            help_text='Optional. Fill in to show a range, e.g. 3,500 – 5,000.')
    description = models.TextField(blank=True, max_length=400)
    in_stock = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers show first.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'photo'

    def __str__(self):
        return Path(self.image.name).name

    def save(self, *args, **kwargs):
        # Phone photos can be 5 MB+; shrink new uploads to a web-friendly JPEG.
        if self.image and not self.image._committed:
            im = ImageOps.exif_transpose(Image.open(self.image)).convert('RGB')
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            buf = BytesIO()
            im.save(buf, 'JPEG', quality=82, optimize=True, progressive=True)
            name = Path(self.image.name).stem + '.jpg'
            self.image.save(name, ContentFile(buf.getvalue()), save=False)
        super().save(*args, **kwargs)
