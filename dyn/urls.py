from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

try:
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('django.contrib.auth.urls')),
        path('', include('app.urls'))
    ]
except ImportError:
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'accounts/', include('django.contrib.auth.urls')),
        url(r'^',include('app.urls')),
    ]

admin.site.site_header = _("DYN APP - Administration")
admin.site.site_title = _("DYN APP")
