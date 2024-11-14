from django.core.management import BaseCommand

from posts.kafka.consumer import process_rating_updates_batch


class Command(BaseCommand):
    help = 'Runs the Kafka consumer to process rating updates'

    def handle(self, *args, **options):
        self.stdout.write("Starting Kafka consumer...")
        process_rating_updates_batch()
