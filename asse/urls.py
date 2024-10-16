from django.urls import path
from .views import BlogListView, BlogDetailView, signup, share_blog_email, like_comment

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:blog_id>/share/', share_blog_email, name='share-blog'),
    path('comments/<int:comment_id>/like/', like_comment, name='like-comment'),
]
