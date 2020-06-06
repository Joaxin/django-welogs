from django import template
# from ..models import Quote
# from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# @register.simple_tag
# def total_quotes():
#     return Quote.published.count()


# @register.inclusion_tag('aphor/latest_quotes.html')
# def show_latest_quotes(count = 5):
#     latest_quotes = Quote.published.order_by('-t_publish')[:count]
#     return {'latest_quotes': latest_quotes}


# @register.simple_tag
# def get_most_commented_quotes(count=5):
#     return Quote.published.annotate(
#                total_comments=Count('comments')
#            ).order_by('-total_comments')[:count]


# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))


@register.filter(is_safe = True)
def custom_markdown(value):
    return mark_safe(markdown.markdown(value,
                              extensions = ['markdown.extensions.extra',
                                            'markdown.extensions.toc',
                                            'markdown.extensions.sane_lists',
                                            'markdown.extensions.nl2br',
                                            'markdown.extensions.codehilite',],
                              safe_mode = True,
                              enable_attributes = False))