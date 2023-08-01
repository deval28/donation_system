from django.core.management.base import BaseCommand
from charity import helpers


class Command(BaseCommand):
    DEFAULT_COUNT = 100
    help = "Creates 100 dummy Contacts for testing purpose"

    def add_arguments(self, parser):
        """
            If no arguments are passed, it will be 100 by default
        """
        parser.add_argument("count", nargs="?", type=int, default=self.DEFAULT_COUNT)

    def handle(self, *args, **options):
        count = options.get('count', self.DEFAULT_COUNT)
        generator = helpers.FakeDataGenerator(count=count)
        generator.generate()
