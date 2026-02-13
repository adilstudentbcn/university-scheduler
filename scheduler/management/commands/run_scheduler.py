from django.core.management.base import BaseCommand
from scheduler.logic import generate_schedule


class Command(BaseCommand):
    help = "Runs the automatic scheduling algorithm"

    def handle(self, *args, **kwargs):
        self.stdout.write("Running scheduler...")
        generate_schedule()
        self.stdout.write(self.style.SUCCESS("Successfully ran scheduler!"))
