from django.test import TestCase
from testcontainers.postgres import PostgresContainer
import psycopg2
import os

class TestContainerSetup(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestContainerSetup, cls).setUpClass()
        # setup PostgreSQL 容器
        cls.container = PostgresContainer()
        cls.container.start()

        # update django database info
        cls.databases = cls.container.get_connection_url()

    @classmethod
    def tearDownClass(cls):
        # 停止容器
        cls.container.stop()