from django.urls import path

from django_blog_olympus.views import BlogHome

urlpatterns = [
    path(r'', BlogHome.as_view(), name='blog_home'),
]
