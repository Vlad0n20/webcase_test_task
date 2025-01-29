import random
from django.core.management.base import BaseCommand


from apps.user.models import User
from apps.user.factories import UserFactory
from apps.group.factories import TeamFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--users_count', type=int, help='Number of users to create')
        parser.add_argument('--teams_count', type=int, help='Number of teams to create')
        parser.add_argument(
            '--create-team-with-new-users',
            action='store_true',
            help='Create team with new users or not',
        )

    def handle(self, *args, **options):
        for _ in range(options['users_count']):
            UserFactory.create()
        users = User.objects.all()
        for _ in range(options['teams_count']):
            if options['create_team_with_new_users']:
                self.stdout.write(self.style.SUCCESS(options['create_team_with_new_users']))
                TeamFactory.create()
            else:
                TeamFactory.create(users=users[:random.randint(2, len(users) - 1)])

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
