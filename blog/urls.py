from django.urls import path

from .views.blog import (
    post_list, post_detail, post_add, edit_post, my_stories,
    post_by_tag, delete_post,
)

from .views import errors


app_name = 'blog'

urlpatterns = [
    path('all/', post_list, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name="post_detail"),
    path('post/new/', post_add, name="post_add"),
    path('post/<slug:slug>/edit/', edit_post, name="post_edit"),
    path('post/delete/<int:year>/<int:month>/<int:day>/<slug:slug>/', delete_post, name="post_delete"),
    path('post/my_stories/', my_stories, name="my_stories"),
    path('all/tags/<slug:slug>/', post_by_tag, name="post_by_tag"),
]

#  Error views
handler404 = errors.handler404