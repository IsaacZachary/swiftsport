import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers show first.')),
            ],
            options={'ordering': ['order', 'name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.CreateModel(
            name='ShopSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(default='Swift Sport', max_length=80)),
                ('tagline', models.CharField(default='Sports & Tactical Gear', max_length=80)),
                ('phone', models.CharField(default='0712 984 925', max_length=30, verbose_name='phone shown on the site')),
                ('whatsapp', models.CharField(default='254712984925', help_text='Country code first, no + or spaces, e.g. 254712984925', max_length=15, verbose_name='WhatsApp number')),
                ('location', models.CharField(default='Airport North Road, Soweto–Baraka, opposite Embakasi Garrison, Embakasi, Nairobi', max_length=200)),
                ('hours', models.CharField(default='Open daily, 8am – 8pm', max_length=80, verbose_name='opening hours')),
            ],
            options={'verbose_name': 'shop details', 'verbose_name_plural': 'shop details'},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('price', models.PositiveIntegerField(default=0, help_text='0 shows "Ask for price".', verbose_name='price (KES)')),
                ('price_max', models.PositiveIntegerField(blank=True, default=0, help_text='Optional. Fill in to show a range, e.g. 3,500 – 5,000.', verbose_name='highest price (KES)')),
                ('description', models.TextField(blank=True, max_length=400)),
                ('in_stock', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers show first.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category')),
            ],
            options={'ordering': ['order', '-created']},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
            options={'ordering': ['order', 'id'], 'verbose_name': 'photo'},
        ),
    ]
