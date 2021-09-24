from django.urls import path

from Edu_news.views import NewsPage, create_news_page, delete_news_page, edit_news_page

urlpatterns = [
    path('news', NewsPage.as_view(), name='news_page'),
    path('addnews', create_news_page, name='addnews'),
    path('deletenews', delete_news_page, name='deletenews'),
    path('editnews', edit_news_page, name='editnews'),

]
