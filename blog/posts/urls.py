from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

app_name = "posts"

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^posts/$', views.post_list, name="list"),
    url(r'^posts/create/$', views.post_create, name="create"),
    url(r'^posts/(?P<slug>[\w-]+)/$', views.post_detail, name="detail"),
    url(r'^posts/(?P<slug>[\w-]+)/edit/$', views.post_update, name="update"),
    url(r'^posts/(?P<slug>[\w-]+)/delete/$', views.post_delete, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
