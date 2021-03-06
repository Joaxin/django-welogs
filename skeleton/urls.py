"""skeleton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('aphor/', include('aphor.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
# from blog.sitemaps import PostSitemap

from .routers import router
from django.views.generic import TemplateView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('users.urls', namespace='accounts')),
    path('', include('op.urls')),
    path('logs/', include('aphor.urls'), name="aphor"),
    path('robots.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
    # path('rosetta/', include('rosetta.urls')),
    path('markdownx/', include('markdownx.urls')),
    # path('api/', include(router.urls)),
    # path('gashapon/', TemplateView.as_view(template_name='gashapon.html')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)