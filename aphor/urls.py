from django.urls import path
from . import views
from .views import MainpageView,SendBlogView

# from aphor.views import Index, Persons, Random, QuotesByPerson, QuotesByCategory, CategoryCreateView, PersonCreateView, QuoteCreateView, LogoutView
# from aphor.api_views import APIPersons, APICategories, APIQuotes, APIQuotesByPerson, APIQuotesByCategory, APIQuotesRandom
app_name = 'aphor'

urlpatterns = [
    path('upload_temp_image/', views.upload_temp_image, name="upload_temp_images"),
    path('', MainpageView.as_view(), name='mainpage'),
    path('publish/', SendBlogView.as_view(), name='sendblog'),
    # path('', views.quote_list, name='quote_list'),
    # path('<int:quote_id>/<slug:quote>/', views.quote_detail, name='quote_detail'),
    # path('<int:quote_id>/<slug:quote>/share/', views.quote_share, name='quote_share'),
    # path('tag/<slug:tag_slug>/', views.quote_list, name='quote_list_by_tag'),
    # path('feed/', LatestQuotesFeed(), name='quote_feed'),
    # path('category/<int:category_pk>/', views.QuotesByCategory, name='quotes_by_category'),
]
