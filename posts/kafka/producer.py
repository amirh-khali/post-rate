import json

from kafka import KafkaProducer

from post_rate import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_SETTINGS['BOOTSTRAP_SERVERS'],
    api_version=(0, 11, 5),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_rating_update_to_kafka(post_id, old_rating, new_rating):
    message = {
        'post_id': post_id,
        'old_rating': old_rating,
        'new_rating': new_rating
    }
    producer.send(settings.KAFKA_SETTINGS['TOPIC'], key=str(post_id).encode('utf-8'), value=message)
