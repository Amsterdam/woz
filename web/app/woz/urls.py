# Packages
from django.conf import settings
from django.conf.urls import url, include
from woz.api.views import WaardeView


waarde_view = WaardeView.as_view()

urlpatterns = [
    url(r'^woz/waarde/', waarde_view, name='waarde'),
    url(r'^status/', include('woz.health.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
