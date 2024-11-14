import json
import time
from collections import defaultdict

from django.core.cache import cache
from kafka import KafkaConsumer

from post_rate import settings

BATCH_SIZE = settings.KAFKA_SETTINGS['BATCH_SIZE']
BATCH_TIMEOUT = settings.KAFKA_SETTINGS['BATCH_TIMEOUT']  # seconds

consumer = KafkaConsumer(
    settings.KAFKA_SETTINGS['TOPIC'],
    bootstrap_servers=settings.KAFKA_SETTINGS['BOOTSTRAP_SERVERS'],
    key_deserializer=lambda k: k.decode('utf-8'),
    value_deserializer=lambda v: json.loads(v),
    group_id=settings.KAFKA_SETTINGS['GROUP_ID'],
    auto_offset_reset=settings.KAFKA_SETTINGS['AUTO_OFFSET_RESET']
)


def process_rating_updates_batch():
    buffer = defaultdict(lambda: {'count_delta': 0, 'total_delta': 0})
    last_flush_time = time.time()

    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
        data = message.value
        post_id = data['post_id']
        old_rating = data['old_rating']
        new_rating = data['new_rating']

        if old_rating is None:
            buffer[post_id]['count_delta'] += 1
            buffer[post_id]['total_delta'] += new_rating
        else:
            buffer[post_id]['total_delta'] += (new_rating - old_rating)

        if len(buffer) >= BATCH_SIZE or time.time() - last_flush_time >= BATCH_TIMEOUT:
            print("batch with size:", len(buffer), "flushed to redis!")
            flush_batch_to_redis(buffer)
            buffer.clear()
            last_flush_time = time.time()


def flush_batch_to_redis(buffer):
    for post_id, deltas in buffer.items():
        count_key = f'post_{post_id}_rating_count'
        total_key = f'post_{post_id}_rating_total'

        count = cache.get(count_key, 0) + deltas['count_delta']
        total = cache.get(total_key, 0) + deltas['total_delta']

        cache.set(count_key, count)
        cache.set(total_key, total)
