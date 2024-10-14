
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
docpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('' , home , name="home"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # init data
    path('api/front/' , include('initapp.urls')),
    
    # videos
    path('api/admin/', include('videos.urls.admin')),
    path('api/front/', include('videos.urls.front')),
    # categories
    path('api/admin/', include('categories.urls.admin')),
    path('api/front/', include('categories.urls.front')),
    # ips
    path('api/', include('allowips.urls.admin')),

    # regular users
    path('api/admin/', include('regularusers.urls.admin')),
    path('api/front/', include('regularusers.urls.front')),
    
    # footer endpoints
    path('api/front/', include('footer.urls')),
    
    # favorites
    path('api/front/' , include('favorites.urls'))
    
] + docpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


