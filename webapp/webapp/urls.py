from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^smartClass/',include('smartClass.urls')),
    url(r'^smartClass/test/','smartClass.views.test'),
    url(r'^testserver/','testserver.views.index'),
    url(r'^smartClass/login','smartClass.views.login'),
    url(r'^smartClass/register','smartClass.views.register'),
    url(r'^smartClass/studentInfo','smartClass.views.studentInfo'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS}),
)#+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
