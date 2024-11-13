from django.core.cache import cache
from django.db.models import Avg

from posts.models import Rating

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def calculate_average_rating(post_id):
    ratings = Rating.objects.filter(post_id=post_id)
    rating_count = ratings.count()
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] or 0

    cache.set(f'post_{post_id}_average_rating', average_rating, CACHE_TIMEOUT)
    cache.set(f'post_{post_id}_rating_count', rating_count, CACHE_TIMEOUT)

    return average_rating, rating_count


def get_cached_rating_data(post_id):
    average_rating = cache.get(f'post_{post_id}_average_rating')
    rating_count = cache.get(f'post_{post_id}_rating_count')

    if average_rating is None or rating_count is None:
        average_rating, rating_count = calculate_average_rating(post_id)

    return average_rating, rating_count
