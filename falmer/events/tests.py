import datetime

from django.test import TestCase

from .utils import parse_date


class DateParsingTest(TestCase):

    def test_spanning_dates(self):
        parsed = parse_date('29th May 9am - 11th June 5pm')
        self.assertEqual(parsed, {
            'start_date': datetime.datetime(2017, 5, 29, 9, 0),
            'end_date': datetime.datetime(2017, 6, 11, 17, 0),
            'is_over_multiple_days': True,
        })
