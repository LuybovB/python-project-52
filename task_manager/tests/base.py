import os
import json
from django.test import TestCase


class BaseTestCase(TestCase):
    FIXTURES_DIR_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures'
    )

    @classmethod
    def get_fixture_path(cls, fixture_name):
        return os.path.join(cls.FIXTURES_DIR_PATH, fixture_name)

    @classmethod
    def load_fixture(cls, fixture_name):
        fixture_path = cls.get_fixture_path(fixture_name)
        with open(fixture_path, 'r') as file:
            return json.load(file)
