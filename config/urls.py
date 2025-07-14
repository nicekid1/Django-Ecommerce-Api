from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import start_payment, verify_payment


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/store/', include('products.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('payment/start/<int:order_id>/', start_payment, name='start_payment'),
    path('payment/verify/<int:order_id>/', verify_payment, name='verify_payment'),
]

