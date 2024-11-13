from django.core.cache import cache
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Rating
from posts.services import get_cached_rating_data
from posts.tasks import update_post_rating
from posts.serializers import PostSerializer, RatingSerializer


class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        for post in queryset:
            post.average_rating, post.rating_count = get_cached_rating_data(post.id)
        return queryset


class RatingCreateUpdateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()

        # Only trigger task if no other rating task is running for the post
        lock_id = f'post_rating_lock_{rating.post.id}'
        if not cache.get(lock_id):
            update_post_rating.delay(rating.post.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
