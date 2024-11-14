from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Rating
from posts.services import get_cached_rating_data
from posts.serializers import PostSerializer, RatingSerializer


class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        for post in queryset:
            count, total = get_cached_rating_data(post.id)
            post.rating_count = count
            post.average_rating = total / count if count > 0 else 0
        return queryset


class RatingCreateUpdateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]
