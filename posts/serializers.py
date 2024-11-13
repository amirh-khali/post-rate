from rest_framework import serializers

from posts.models import Post, Rating


class PostSerializer(serializers.ModelSerializer):
    rating_count = serializers.IntegerField(required=False)
    average_rating = serializers.FloatField(required=False)
    user_rating = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'rating_count', 'average_rating', 'user_rating']
        read_only_fields = ['average_rating', 'user_rating']

    def get_user_rating(self, obj, *args, **kwargs):
        user_id = self.context.get('request').parser_context.get('kwargs').get('user_id')
        if user_id:
            rating = Rating.objects.filter(post=obj, user_id=user_id).first()
            return rating.score if rating else None
        return None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user_id', 'post', 'score']
        extra_kwargs = {'score': {'min_value': 0, 'max_value': 5}}

    def create(self, validated_data):
        user_id = validated_data['user_id']
        post = validated_data['post']
        score = validated_data['score']
        rating, created = Rating.objects.update_or_create(user_id=user_id, post=post, defaults={'score': score})
        return rating
