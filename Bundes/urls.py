from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, static
from django.conf import settings
from bundesinfo import views as bundesinfo_views

urlpatterns = [
    url(r'^$', bundesinfo_views.IndexPage.as_view(), name='index_page'),
    url(r'^bundes-info/', include('bundesinfo.urls', namespace='bundesinfo')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
