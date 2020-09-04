from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecommerce/api/', include('ecommerce.urls')),
    path('core/api/', include('core.urls')),
]
