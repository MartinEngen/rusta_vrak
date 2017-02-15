# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns

from frontpage.views import index
urlpatterns = [
    url(r'^$', index),
    url(r'^', include('cars.urls', namespace='cars')),
    url(r'^', include('booking.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
)

