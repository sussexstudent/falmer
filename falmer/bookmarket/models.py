import arrow
from django.conf import settings
from django.db import models
from django.db.models import Q
from django_extensions.db.fields import AutoSlugField

from falmer.core.models import TimeStampedModel
from falmer.matte.models import MatteImage

LISTING_STATUS = (
    ('DRAFT', 'Draft'),
    ('READY', 'Ready'),
    ('EXPIRED', 'Expired'),
)


class ListingSection(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = AutoSlugField(populate_from='title', blank=False, null=False, unique=True)

    def __str__(self):
        return self.title


class ListingsQuerySet(models.QuerySet):
    def get_public_or_owned_by_user(self, pk, user):
        if user.is_authenticated:
            return self.get(Q(listing_user=user) | Q(state='READY', listed_at__gte=arrow.utcnow().shift(days=-90).datetime), pk=pk, )
        else:
            return self.get(state='READY', listed_at__gte=arrow.utcnow().shift(days=-90).datetime, pk=pk)

    def public(self):
        return self.filter(state='READY', listed_at__gte=arrow.utcnow().shift(days=-90).datetime)

    def created_by(self, user):
        return self.filter(listing_user=user)

    def get_owned_by_user(self, listing_id, owner):
        return self.get(pk=listing_id, listing_user=owner)


class ListingContactRequester(TimeStampedModel, models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Listing(TimeStampedModel, models.Model):
    objects = ListingsQuerySet.as_manager()

    book_title = models.CharField(max_length=255, null=False)
    book_author = models.TextField(null=False, default='')

    description = models.TextField(default='', blank=True, null=False)

    listing_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    section = models.ForeignKey(ListingSection, on_delete=models.CASCADE)

    buy_price = models.DecimalField(decimal_places=2, max_digits=4, null=False)

    state = models.CharField(max_length=10, default='DRAFT')

    contact_details = models.TextField(null=False, default='')

    listing_change_canary = models.IntegerField(default=0, null=False, editable=False)
    listed_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    images = models.ManyToManyField(MatteImage)
    contact_requesters = models.ManyToManyField(settings.AUTH_USER_MODEL, through=ListingContactRequester, through_fields=('listing', 'user'))

    def featured_image(self):
        if self.images.count() > 0:
            return self.images.last()
        else:
            return None

    def transition_state(self, next_state):
        if self.state != 'READY' and next_state == 'READY':
            self.listed_at = arrow.utcnow().datetime

        self.state = next_state

    def can_see_contact_details(self, user):
        if self.listing_user == user:
            return True

        if self.listingcontactrequester_set.filter(user=user).exists():
            return True

        return False

    def record_request(self, user):
        if not self.can_see_contact_details(user):
            ListingContactRequester.objects.create(
                listing=self,
                user=user,
            )


# class ListingMessage(TimeStampedModel):
#     request = models.ForeignKey(ListingRequest, related_name='offers')
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     body = models.TextField()
#
#
# class ListingOffer(models.Model):
#     request = models.ForeignKey(ListingRequest, related_name='offers')
#     price = models.DecimalField(decimal_places=2)
#
#     seller_confirmed = models.BooleanField(default=False)
#     buyer_confirmed = models.BooleanField(default=False)
