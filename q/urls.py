from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_reg_page),
    path('create_user', views.create_user),
    path('login', views.login),
    path('success', views.success),
    path('quotes', views.quotes),
    path('create_quote', views.create_quote),
    path('eliminate_quote/<int:quote_id>', views.eliminate_quote),
    path('profile/<int:user_id>', views.profile),
    path('edit_quote/<int:quote_id>', views.edit_quote),
    path('edit/<int:quote_id>', views.edit),
    path('favorite/<int:quote_id>', views.favorite),
    path('unfavorite/<int:quote_id>', views.unfavorite),
    path('logout', views.logout),

]