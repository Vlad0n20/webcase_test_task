from django.core.management.base import BaseCommand


from apps.user.factories import UserFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--users_count', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        users_count = options['users_count'] if options['users_count'] else 10
        for _ in range(users_count):
            UserFactory.create()
        self.stdout.write(self.style.SUCCESS('Successfully created {} users'.format(users_count)))
