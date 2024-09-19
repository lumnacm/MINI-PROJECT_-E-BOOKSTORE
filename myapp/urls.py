
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bookstoremanagement import settings
from myapp import views

urlpatterns = [
    path('',views.public),
    path('login',views.login),
    path('userreg',views.userreg),
    path('adminhome',views.admin_home),
    path('blockuser/<id>',views.blockuser),
    path('unblockuser/<id>',views.unblockuser),
    path('admin_view_user',views.admin_view_user),
    path('admin_add_category',views.admin_add_category),
    path('admin_add_books',views.admin_add_books),
    path('admin_view_books',views.admin_view_books),
    path('admin_delete_book/<id>',views.admin_delete_book),
    path('admin_edit_books/<id>',views.admin_edit_books),
    path('admin_edit_books_post', views.admin_edit_books_post),


    path('user_home', views.user_home),

]

