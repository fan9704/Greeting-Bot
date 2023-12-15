from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import ProgrammingError
from django.conf import settings
from pymongo import MongoClient
import os


class Command(BaseCommand):
    help = 'Create a PostgreSQL database named "test" for testing'

    def handle(self, *args, **options):
        if settings.DATABASES['default'].get("ENGINE") == "djongo":
            client = MongoClient(host=os.getenv("MONGO_DB_URL"), port=int(os.getenv("MONGO_DB_PORT", 27017)))
            try:
                # Check if the 'test' database already exists
                database_exists = client['test'].name in client.list_database_names()
            except:
                database_exists = False

            if not database_exists:
                # Create the 'test' database
                client['test']
                self.stdout.write(self.style.SUCCESS('Database "test" created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Database "test" already exists.'))
        elif settings.DATABASES['default'].get("ENGINE") == "django.db.backends.postgresql":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT datname FROM pg_database WHERE datname = 'test';")
                    database_exists = cursor.fetchone()
            except ProgrammingError:
                database_exists = False

            if not database_exists:
                with connection.cursor() as cursor:
                    cursor.execute('CREATE DATABASE TEST;')
                self.stdout.write(self.style.SUCCESS('Database "test" created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Database "test" already exists.'))
