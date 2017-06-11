from django.test import TestCase

from .utils import parse_date


class DateParsingTest(TestCase):

    def test_spanning_dates(self):
        parsed = parse_date('29th May 9am - 11th June 5pm')
        self.assertEqual(parsed, {
            'start_date': '',
            'end_date': '',
            'is_multi_day': True,
        })
