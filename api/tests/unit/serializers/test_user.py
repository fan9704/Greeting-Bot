import logging
import datetime

from rest_framework.exceptions import ValidationError
from django.test import TestCase
from api.serializers.user import SimpleMessageSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserSerializerTestCase(TestCase):
    def test_user_serializer(self):
        user_data = {
            'first_name': 'Cat',
            'last_name': 'Tom',
            'gender': 'm',
            'date_of_birth': datetime.date(2023, 9, 1),
            'email': "u1@gmail.com",
        }
        serializer = UserSerializer(data=user_data)
        serializer.is_valid()

        # Assert
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['first_name'], 'Cat')
        self.assertEqual(serializer.validated_data['last_name'], 'Tom')
        self.assertEqual(serializer.validated_data['gender'], 'm')
        self.assertEqual(serializer.validated_data['date_of_birth'], datetime.date(2023, 9, 1))
        self.assertEqual(serializer.validated_data['email'], "u1@gmail.com")
        logger.debug("Complete User Serializer Test")

        # Input Invalid JSON Data
        invalid_user_data = {
            'gender': '',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserSerializer(data=invalid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        logger.debug("Complete User Invalid Serializer Test")

    def test_simple_message_serializer(self):
        message_data = {
            "message": "Happy Birthday",
            "username": "Cat"
        }
        serializer = SimpleMessageSerializer(data=message_data)
        serializer.is_valid()
        # Assert
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'Cat')
        self.assertEqual(serializer.validated_data['message'], 'Happy Birthday')
        logger.debug("Complete Simple Message Serializer Test")

        # Input Invalid JSON Data
        invalid_user_data = {
            "message": "",
            "username":""
        }
        serializer = SimpleMessageSerializer(data=invalid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        logger.debug("Complete Simple Message Invalid Serializer Test")