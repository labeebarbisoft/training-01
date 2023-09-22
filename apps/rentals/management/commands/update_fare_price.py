from django.core.management.base import BaseCommand
from django.db.models import F
from apps.rentals.models import FareRate


class Command(BaseCommand):
    help = "Update the fare price of instances by a given percentage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--perc",
            type=int,
            help="Percent increase in price",
        )

    def handle(self, *args, **options):
        updated_instances = FareRate.objects.update(
            fare=F("fare") * (1 + 0.01 * options["perc"])
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_instances} instances of FareRate"
            )
        )
