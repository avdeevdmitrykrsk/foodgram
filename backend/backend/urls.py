from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

from content.views import ShortLinkView

api_urlpatterns = [
    path('', include('users.urls')),
    path('', include('content.urls'))
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    path('admin/', admin.site.urls),
    path('s/<slug:short>/', ShortLinkView.as_view(), name='short-link'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
