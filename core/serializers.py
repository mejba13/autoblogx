from rest_framework import serializers
from .models import Post, Media, SEOMeta

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class SEOMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOMeta
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    seo = SEOMetaSerializer(source='seometa', read_only=True)
    media = MediaSerializer(source='media_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'body', 'category', 'created_at',
            'featured_image', 'seo', 'media'
        ]
