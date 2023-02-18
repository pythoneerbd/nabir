from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('single_article/<int:id>/',views.single_article, name='single_article'),
    path('category/<slug:slug>/<int:id>/',views.article_category, name='article_category'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('about-us/',views.about_us, name='about_us'),
    path('contact-us/',views.contact_us, name='contact_us'),



]