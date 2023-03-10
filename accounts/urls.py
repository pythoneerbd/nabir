from django.urls import path
from accounts.views import registration_view, \
    logout_view, \
    login_view, \
    account_view, \
    getAuthor, \
    change_password,\
    post_create,\
    PostUpdate

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('profile/', account_view, name='profile'),
    path('author-profile/<username>', getAuthor, name='author'),
    # Authentication and Authorization
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('change-password/',change_password, name='change_password'),
    path('post_create/', post_create, name='post_create'),
    path('post_update/<int:id>', PostUpdate, name='post_update'),
    # Accounts utils
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    # path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    #      name='password_change_done'),
    #
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
    #      name='password_change'),
    #
    # path('password_reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
    #      name='password_reset_done'),
    #
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='registration/password_reset_confermation.html'
    # ),
    #      name='password_reset_confirm'),
    #
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
    #      name='password_reset'),
    #
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #      name='password_reset_complete'),

    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
]
