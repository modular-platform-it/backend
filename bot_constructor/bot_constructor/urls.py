import typing

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

URL = typing.Union[URLPattern, URLResolver]
URLList = typing.List[URL]

urlpatterns: URLList = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
