import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from purchases.models import Cart


class Command(BaseCommand):

    def handle(self, *args, **options):
        json_path = Path(settings.INITIAL_DATA_DIR, "ingredients.json")
        with open(
                json_path,
                'r',
                encoding='utf-8'
        ) as json_file:
            json_dict: dict = json.load(json_file)

        Cart.objects.bulk_create([Cart(
            name=cart['name'],
            measurement_unit=cart['measurement_unit'])
            for cart in json_dict])
