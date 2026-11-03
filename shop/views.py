from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Product, ShopSettings


def shop_data():
    s = ShopSettings.load()
    products = Product.objects.select_related('category').prefetch_related('images')
    return {
        'settings': {
            'shopName': s.shop_name, 'tagline': s.tagline, 'phone': s.phone,
            'whatsapp': s.whatsapp, 'location': s.location, 'hours': s.hours,
        },
        'products': [{
            'id': str(p.pk), 'name': p.name, 'category': p.category.name,
            'price': p.price, 'priceMax': p.price_max, 'description': p.description,
            'images': [im.image.url for im in p.images.all()], 'inStock': p.in_stock,
        } for p in products],
    }


@require_GET
def home(request):
    return render(request, 'shop/index.html', {'shop_data': shop_data()})


@require_GET
def products_json(request):
    return JsonResponse({'data': shop_data()})
