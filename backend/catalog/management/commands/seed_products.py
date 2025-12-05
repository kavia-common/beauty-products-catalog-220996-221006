from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Seeds sample categories, tags and products."

    # PUBLIC_INTERFACE
    def handle(self, *args, **options):
        """Load bundled fixtures for a meaningful preview."""
        # Using 'catalog' app fixture; safe to run multiple times (duplicates use fixed PKs)
        call_command("loaddata", "products", app_label="catalog")
        self.stdout.write(self.style.SUCCESS("Seeded sample products."))
