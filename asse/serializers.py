from rest_framework import serializers
from .models import BlogPost, Tag, Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'created_at', 'tags']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'user', 'content', 'created_at', 'likes']
