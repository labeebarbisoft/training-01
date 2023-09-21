from django.core.management.base import BaseCommand
from apps.rentals.models import VehicleBookingRequest
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Check and update the status of old VehicleBookingRequest instances"

    def handle(self, *args, **options):
        two_days_ago = datetime.now() - timedelta(days=2)

        pending_instances = VehicleBookingRequest.objects.filter(
            status="pending", pickup_date__lte=two_days_ago
        )

        for instance in pending_instances:
            instance.status = "closed"
            instance.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {len(pending_instances)} instances"
            )
        )
