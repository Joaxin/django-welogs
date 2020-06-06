from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Quote


class LatestQuotesFeed(Feed):
    title = 'My blog'
    link = '/aphor/'
    description = 'New posts of my blog.'

    def items(self):
        return Quote.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
