import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    help = "Waits for database to be available"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False

        while not db_up:
            try:
                # Пробуємо підключитись до БД
                connections["default"].ensure_connection()
                db_up = True
            except (Psycopg2Error, OperationalError):
                # Psycopg2Error: БД ще не запустилась
                # OperationalError: БД запустилась але ще не приймає з'єднання
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
