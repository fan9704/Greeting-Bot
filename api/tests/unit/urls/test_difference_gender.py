import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class DifferenceGenderURLTest(TestCase):
    def testCallbackURL(self):
        url = reverse("Difference-Gender-API")
        self.assertEqual(url, "/api/difference-gender/")
        logger.debug("Complete Difference Gender URL Test")
