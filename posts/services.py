from django.core.cache import cache

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def get_cached_rating_data(post_id):
    count = cache.get(f'cached_post_{post_id}_rating_count')
    total = cache.get(f'cached_post_{post_id}_rating_total')

    if count is None or total is None:
        count = cache.get(f'post_{post_id}_rating_count', 0)
        total = cache.get(f'post_{post_id}_rating_total', 0)

        cache.set(f'cached_post_{post_id}_rating_count', count, CACHE_TIMEOUT)
        cache.set(f'cached_post_{post_id}_rating_total', total, CACHE_TIMEOUT)

    return count, total
