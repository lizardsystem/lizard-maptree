# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.contrib import admin

from lizard_maptree.views import MaptreeHomepageView

urlpatterns = patterns(
    '',
    url(r'^$', MaptreeHomepageView.as_view(),
        name='lizard_maptree.homepage'),
    # ^^^ Actually, we're really called from lizard_wms's urls
    )

if getattr(settings, 'LIZARD_MAPTREE_STANDALONE', False):
    admin.autodiscover()
    urlpatterns += patterns(
        '',
        (r'^map/', include('lizard_map.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'', include('django.contrib.staticfiles.urls')),
    )
