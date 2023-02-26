from django.core.management.base import BaseCommand
from app.contact import ContactCallbackBackend


class Command(BaseCommand):
    help = 'Runs the backend for the kafka tasks'

    def handle(self, *args, **kwargs):
        backend = ContactCallbackBackend()
        backend.run()

