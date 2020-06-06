from django.contrib.sitemaps import Sitemap
from .models import MiniBlog


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return MiniBlog.published.all()

    def lastmod(self, obj):
        return obj.t_update
