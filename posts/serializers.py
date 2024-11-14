from rest_framework import serializers

from posts.models import Post, Rating
from posts.services import update_post_rating_data


class PostSerializer(serializers.ModelSerializer):
    rating_count = serializers.IntegerField(required=False, read_only=True)
    average_rating = serializers.FloatField(required=False, read_only=True)
    user_rating = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_by', 'rating_count', 'average_rating', 'user_rating']
        read_only_fields = ['created_by', 'rating_count', 'average_rating', 'user_rating']

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user:
            rating = Rating.objects.filter(post=obj, user=user).first()
            return rating.score if rating else None
        return None

    def create(self, validated_data):
        title = validated_data['title']
        content = validated_data['content']
        created_by = self.context['request'].user
        post, created = Post.objects.update_or_create(title=title, content=content, created_by=created_by)
        return post


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['post', 'score']
        extra_kwargs = {'score': {'min_value': 0, 'max_value': 5}}

    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']
        new_score = validated_data['score']
        existing_rating = Rating.objects.filter(user=user, post=post).first()

        if existing_rating:
            old_score = existing_rating.score
        else:
            old_score = None

        # Update Redis data
        update_post_rating_data(post.id, old_score, new_score)

        rating, created = Rating.objects.update_or_create(user=user, post=post, defaults={'score': new_score})
        return rating
