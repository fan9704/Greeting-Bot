import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class LineBotURLTest(TestCase):
    def testCallbackURL(self):
        url = reverse("LINE-Bot-Callback")
        self.assertEqual(url, "/api/callback/")
        logger.debug("Complete LINE Bot Callback URL Test")
