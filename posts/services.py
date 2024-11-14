from django.core.cache import cache
from django.db.models import Sum

from posts.models import Rating

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def update_post_rating_data(post_id, old_rating, new_rating):
    count = cache.get(f'post_{post_id}_rating_count')
    total = cache.get(f'post_{post_id}_rating_total')

    if count is None or total is None:
        ratings = Rating.objects.filter(post_id=post_id)
        count = ratings.count()
        total = ratings.aggregate(total=Sum('score'))['total'] or 0

    if old_rating is None:
        count += 1
        total += new_rating
    else:
        total += (new_rating - old_rating)

    cache.set(f'post_{post_id}_rating_count', count)
    cache.set(f'post_{post_id}_rating_total', total)

    return count, total


def get_cached_rating_data(post_id):
    count = cache.get(f'cached_post_{post_id}_rating_count')
    total = cache.get(f'cached_post_{post_id}_rating_total')

    if count is None or total is None:
        count, total = update_post_rating_data(post_id, 0, 0)  # not going to change anything

        cache.set(f'cached_post_{post_id}_rating_count', count, CACHE_TIMEOUT)
        cache.set(f'cached_post_{post_id}_rating_total', total, CACHE_TIMEOUT)

    return count, total
