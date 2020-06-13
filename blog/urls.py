from django.urls import path

from .views import (
    post_list, post_detail, posts_page, post_share,
    add_category, post_add,
)


app_name = 'blog'

urlpatterns = [
    path('category/add/', add_category, name="add_post_category"),
    path('category/<slug:slug>/', posts_page, name="category"),
    path('add/', post_add, name="add_post"),
    path('all/', post_list, name="all_posts"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name="post_detail"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_share, name="post_share"),
]