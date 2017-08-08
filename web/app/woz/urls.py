# Packages
from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    url(r'^status/', include('health.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
