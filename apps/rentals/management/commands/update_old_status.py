from django.core.management.base import BaseCommand
from apps.rentals.models import VehicleBookingRequest
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Check and update the status of old VehicleBookingRequest instances"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days-back",
            type=int,
            default=2,
            help="Number of days to check back (default is 2)",
        )

    def handle(self, *args, **options):
        days_back = datetime.now() - timedelta(days=options["days_back"])

        pending_instances = VehicleBookingRequest.objects.filter(
            status="pending", pickup_date__lte=days_back
        ).update(status="closed")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {pending_instances} instances of VehicleBookingRequest"
            )
        )
