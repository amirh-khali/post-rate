from django.core.cache import cache

from posts.services import calculate_average_rating
from post_rate.celery import app


@app.task
def update_post_rating(post_id):
    lock_id = f'post_rating_lock_{post_id}'
    print(lock_id)
    if cache.add(lock_id, 'locked', timeout=30):
        try:
            calculate_average_rating(post_id)
        finally:
            cache.delete(lock_id)
    else:
        print(f"Task skipped: Another rating calculation in progress for post {post_id}")
