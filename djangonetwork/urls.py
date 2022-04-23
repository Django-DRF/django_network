from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('actions/', include('djangoapps.post.urls')),
    path('inbox/', include('djangoapps.inbox.urls')),
    path('', include('djangoapps.core.urls')),
    path('', include('djangoapps.userprofile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
