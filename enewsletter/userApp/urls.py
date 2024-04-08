from django.contrib import admin
from django.urls import path
from userApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("login_page/", views.login_page, name="login_page"),
    path("signup/", views.signup, name="signup"),
    path("userPage/", views.userPage, name="userPage"),
    path("adminPage/", views.adminPage, name="adminPage"),
    path("save_data/", views.save_data, name="save_data"),  
    path("check_data/",views.check_data,name="check_data"),
    path("circulateNews/", views.circulateNews, name='circulateNews'),
    path("adminPage/logout/", views.logout_page, name="logout"),
    path("userPage/logout/", views.logout_page, name="logout"),
    path("logout_page/", views.logout_page, name="logout"),  
    path("userPage/messagePage", views.messagePage, name="messagePage"),
    path('bookmark_newsletter/', views.bookmark_newsletter, name='bookmark_newsletter'),
    path('bookmarked_messages/', views.bookmarked_messages, name='bookmarked_messages'),
    path('admin_inbox/', views.admin_inbox, name='admin_inbox'),
    path('delete_newsletter/', views.delete_newsletter, name='delete_newsletter'),
    path('edit_message_page/', views.edit_message_page, name='edit_message_page'),
    path('update_newsletter/<int:newsletter_id>/', views.update_newsletter, name='update_newsletter'),
    path('api/generate-message/', views.generate_message_api, name='generate_message_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
