import logging
import os

from django.core.management import call_command
from django.test import TransactionTestCase
from django.db import connections
from django.conf import settings
from psycopg2 import sql
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class CreateTestDatabaseTestCase(TransactionTestCase):
    def test_create_test_database(self):
        call_command('create_test_db')
        if settings.DATABASES['default'].get("ENGINE") == "djongo":
            client = MongoClient(host=os.getenv("MONGO_DB_URL"), port=int(os.getenv("MONGO_DB_PORT", 27017)))
            database = client['test']

            # Check if database exists
            database_exists = database.name in client.list_database_names()

            self.assertIsNotNone(database_exists)
        elif settings.DATABASES['default'].get("ENGINE") == "django.db.backends.postgresql":

            with connections['default'].cursor() as cursor:
                query = sql.SQL("SELECT datname FROM pg_database WHERE datname = %s;")
                cursor.execute(query, ['test'])
                database_exists = cursor.fetchone()

            self.assertIsNotNone(database_exists)

    def tearDown(self):
        if settings.DATABASES['default'].get("ENGINE") == "djongo":
            client = MongoClient('localhost', 27017)
            client.drop_database('test')
        elif settings.DATABASES['default'].get("ENGINE") == "django.db.backends.postgresql":
            with connections['default'].cursor() as cursor:
                query = sql.SQL("DROP DATABASE IF EXISTS test;")
                cursor.execute(query)
