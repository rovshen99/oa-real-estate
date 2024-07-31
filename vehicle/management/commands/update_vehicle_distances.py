import asyncio

from django.core.management.base import BaseCommand
from vehicle.scripts.update_vehicle_distances import update_vehicle_distances


class Command(BaseCommand):
    help = 'Updates vehicle distances from Traccar'

    def handle(self, *args, **kwargs):
        asyncio.run(update_vehicle_distances())
        self.stdout.write(self.style.SUCCESS('Successfully updated vehicle distances'))
