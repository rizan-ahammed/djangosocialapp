from django.urls import path, include
from posts import views

app_name = "posts"


urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("delete/<int:id>/", views.delete_post, name="delete_post"),
    path("edit/<int:id>/", views.edit_post, name="edit_post"),
    path("draft/<int:id>/", views.draft_post, name="draft_post"),
]
