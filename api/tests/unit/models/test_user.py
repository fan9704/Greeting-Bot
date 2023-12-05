import datetime
import logging

from api.models import User
from django.test import TestCase

logger = logging.getLogger(__name__)


class UserModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(
            first_name="Cat",
            last_name="Tom",
            date_of_birth=datetime.date(2023, 9, 1),
            email="u1@gmail.com"
        )
        self.u2 = User.objects.create(
            first_name="Mouse",
            last_name="Jelly",
            date_of_birth=datetime.date(2023, 8, 24),
            email="u2@gmail.com"
        )

    def testUserModel(self):
        self.assertEqual(self.u1.date_of_birth, datetime.date(2023, 9, 1))
        self.assertEqual(self.u2.date_of_birth, datetime.date(2023, 8, 24))
        logger.debug("Complete User Date of Birth Model Test")

        self.assertEqual(self.u1.email, "u1@gmail.com")
        self.assertEqual(self.u2.email, "u2@gmail.com")
        logger.debug("Complete User Email Model Test")

        self.assertEqual(self.u1.last_name, 'Tom')
        self.assertEqual(self.u2.last_name, 'Jelly')
        logger.debug("Complete User Lastname Model Test")

        self.assertEqual(self.u1.first_name, "Cat")
        self.assertEqual(self.u2.first_name, "Mouse")
        logger.debug("Complete User Firstname Model Test")

    def tearDown(self):
        User.objects.all().delete()
