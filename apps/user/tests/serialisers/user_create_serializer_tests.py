from django.test import TestCase

from apps.user.serializers import UserCreateSerializer


class UserCreateSerializerTestCase(TestCase):
    def setUp(self):
        self.first_name = 'test first name'
        self.last_name = 'test last name'
        self.email = 'test email'
        self.password = 'test password'
        self.data = {
            'first_name':  'first name',
            'last_name':  'last name',
            'email':  'email@gmial.com',
            'password':  'password',
        }

    def test_it_validates_first_name(self):
        self.data['first_name'] = '!test'
        serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['first_name'][0],
            "First name cannot contain special characters."
        )

    def test_validated_method(self):
        first_user = UserCreateSerializer(data=self.data)
        self.assertTrue(first_user.is_valid())
        first_user.save()

        serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['email'][0]),
            "User with this Email already exists."
        )

    def test_password_is_write_only(self):
        serializer = UserCreateSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('password', serializer.data)
        self.assertNotIn('password', serializer.errors)
