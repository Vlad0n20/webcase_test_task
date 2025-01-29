from django.test import TestCase

from apps.user.models import User
from apps.user.factories import UserFactory


class UserModelTestCase(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.first_name = 'test first name'
        self.last_name = 'test last name'
        self.email = 'test email'
        self.user = UserFactory(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email
        )

    def test_it_has_first_name_field(self):
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(
            self.user._meta.get_field("first_name").verbose_name, "first name"
        )

    def test_it_has_last_name_field(self):
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(
            self.user._meta.get_field("last_name").verbose_name, "last name"
        )

    def test_it_has_email_field(self):
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(
            self.user._meta.get_field("email").verbose_name, "Email"
        )

    def test_email_is_unique(self):
        self.assertEqual(
            self.user._meta.get_field("email").unique, True
        )

    def test_it_has_is_active_field(self):
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(
            self.user._meta.get_field("is_active").verbose_name, "active"
        )

    def test_it_has_is_staff_field(self):
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(
            self.user._meta.get_field("is_staff").verbose_name, "staff status"
        )

    def test_it_has_is_superuser_field(self):
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(
            self.user._meta.get_field("is_superuser").verbose_name, "superuser status"
        )

    def test_it_has_date_joined_field(self):
        self.assertEqual(
            self.user._meta.get_field("date_joined").verbose_name, "date joined"
        )

    def test_it_has_last_login_field(self):
        self.assertEqual(
            self.user._meta.get_field("last_login").verbose_name, "last login"
        )

    # Methods

    def test_str_method(self):
        self.assertEqual(str(self.user), f'{self.first_name} {self.last_name}')

    def test_ordering_working(self):
        users = User.objects.all()
        for index, user in enumerate(users):
            if index == 0:
                continue
            self.assertLess(user.id, users[index - 1].id)
