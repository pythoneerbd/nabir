from django.urls import path

from . import views

app_name = 'newsletters'

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe, name='subscribe'),
    path('unsubscribe/',views.newsletter_unsubscribe, name='unsubscribe'),

]