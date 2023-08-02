from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('auth/', include('authentication.urls')),
    path('api/', include('api.urls')),
    path('rooms/', include('rooms.urls')),
]

# instead of adding the path like above we append it
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
