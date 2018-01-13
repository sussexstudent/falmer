import arrow
from django.contrib.auth.models import Permission
from django.test.testcases import TestCase

from falmer.auth.models import FalmerUser
from .models import Event


class EventManagementTestCase(TestCase):
    def setUp(self):
        self.sports_tryouts_event = Event.objects.create(
            title='Sports Tryouts',
            start_time=arrow.utcnow().datetime,
            end_time=arrow.utcnow().shift(hours=3).datetime,
        )

        self.badminton_tryout = Event.objects.create(
            title='Badminton Tryouts',
            start_time=arrow.utcnow().datetime,
            end_time=arrow.utcnow().shift(hours=1).datetime,
        )

        self.ruby_tryout = Event.objects.create(
            title='Ruby Tryouts',
            start_time=arrow.utcnow().shift(hours=1).datetime,
            end_time=arrow.utcnow().shift(hours=2).datetime,
        )

        self.user_with_perm = FalmerUser.objects.create_user(identifier='website@sussexstudent.com')

        change_perm = Permission.objects.get(codename='change_event')
        self.user_with_perm.user_permissions.add(change_perm)

    def test_moving_children(self):
        # move event under another
        self.assertTrue(self.ruby_tryout.move_under(self.sports_tryouts_event, self.user_with_perm))
        self.ruby_tryout.save()

        # move event with children under another
        self.assertFalse(self.sports_tryouts_event.move_under(self.badminton_tryout, self.user_with_perm))
