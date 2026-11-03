from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from shop import views

admin.site.site_header = 'Swift Sport · Shop manager'
admin.site.site_title = 'Swift Sport admin'
admin.site.index_title = 'Manage products and shop details'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/products', views.products_json, name='products-json'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
