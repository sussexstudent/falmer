import arrow
from dateutil import tz
from django.db import models, transaction
from django_extensions.db.fields import AutoSlugField
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel, \
    ObjectList
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from falmer.links.utils import LinkedMetadata
from falmer.matte.models import MatteImage, RemoteImage
from falmer.studentgroups.models import StudentGroup


class Bundle(models.Model):
    name = models.CharField(max_length=72)

    def __str__(self):
        return self.name


class BrandingPeriod(models.Model):
    name = models.CharField(max_length=72)
    website_link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=72)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=72)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255, default='')
    short_description = models.TextField(default='')
    featured_image = models.ForeignKey(MatteImage, null=True, blank=True, on_delete=models.SET_NULL)


    custom_panels = [
        MultiFieldPanel([
            FieldPanel('name', classname='title'),
            FieldPanel('website_link'),
            FieldPanel('short_description'),
            ImageChooserPanel('featured_image')
        ], heading='The basics'),
    ]

    edit_handler = ObjectList(custom_panels)


    def __str__(self):
        return self.name


class AutoLocationDisplayToVenue(models.Model):
    venue = models.ForeignKey(Venue, null=False)
    location = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.location


class Event(models.Model):
    FREE = 'FREE'
    PAID = 'PAID'
    NA = 'NA'
    COST_CHOICES = (
        (FREE, 'Free'),
        (PAID, 'Paid'),
        (NA, 'n/a'),
    )

    NATIVE = 'NT'
    TICKET_TYPE_CHOICES = (
        (NA, 'n/a'),
        (NATIVE, 'Native'),
    )

    SOFT_DRINKS_ALCOHOL = 'AV'
    NO_ALCOHOL = 'NO'
    NOT_ALCOHOL_FOCUSED = 'NF'

    ALCOHOL_CHOICES = (
        (SOFT_DRINKS_ALCOHOL, 'Soft drinks & alcohol available'),
        (NO_ALCOHOL, 'No alcohol'),
        (NOT_ALCOHOL_FOCUSED, 'Not alcohol focused'),
    )

    LIMITED_AVAILABILITY = 'LA'
    SOLD_OUT = 'SO'
    TICKET_LEVEL_CHOICES = (
        (NA, 'Not applicable'),
        (LIMITED_AVAILABILITY, 'Limited availability'),
        (SOLD_OUT, 'Sold out'),
    )

    parent = models.ForeignKey('self', default=None, null=True, blank=True, related_name='children')

    title = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    featured_image = models.ForeignKey(MatteImage, null=True, blank=True, on_delete=models.SET_NULL)
    url = models.URLField(blank=True, default='')
    social_facebook = models.URLField(blank=True, default='')
    kicker = models.CharField(max_length=255, default='', blank=True)
    location_display = models.CharField(max_length=255, default='', blank=True)
    embargo_until = models.DateTimeField(null=True, blank=True)

    venue = models.ForeignKey(Venue, blank=True, null=True)
    short_description = models.TextField(default='')
    body = RichTextField(default='', blank=True)
    student_group = models.ForeignKey(StudentGroup, null=True, blank=True, default=None)

    is_over_18_only = models.BooleanField(default=False)
    ticket_level = models.CharField(max_length=2, choices=TICKET_LEVEL_CHOICES, default=NA)
    cost = models.CharField(max_length=10, choices=COST_CHOICES, default=NA)
    alcohol = models.CharField(max_length=2, choices=ALCOHOL_CHOICES, default=NOT_ALCOHOL_FOCUSED)

    ticket_type = models.CharField(max_length=2, choices=TICKET_TYPE_CHOICES, default=NA)
    ticket_data = models.TextField(default='', blank=True)

    suitable_kids_families = models.BooleanField(default=False)
    just_for_pgs = models.BooleanField(default=False)

    bundle = models.ForeignKey(Bundle, null=True, blank=True)
    brand = models.ForeignKey(BrandingPeriod, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    type = models.ForeignKey(Type, null=True, blank=True)

    custom_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldRowPanel([
                FieldPanel('start_time'),
                FieldPanel('end_time'),
            ]),
            FieldPanel('embargo_until'),
            ImageChooserPanel('featured_image')
        ], heading='The basics'),
        MultiFieldPanel([
            FieldPanel('kicker'),
            FieldPanel('short_description'),
            FieldPanel('body'),
            FieldPanel('location_display'),
            FieldPanel('venue'),
        ], heading='More details'),
        MultiFieldPanel([
            FieldPanel('social_facebook'),
            FieldPanel('url'),
        ], heading='Social'),
        MultiFieldPanel([
            FieldPanel('is_over_18_only'),
            FieldPanel('ticket_level'),
            FieldPanel('cost'),
            FieldPanel('alcohol'),
            FieldPanel('suitable_kids_families'),
            FieldPanel('just_for_pgs'),
        ], heading='About the event itself'),
        MultiFieldPanel([
            FieldPanel('ticket_type'),
            FieldPanel('ticket_data'),
        ], heading='Ticketing'),
        MultiFieldPanel([
            FieldPanel('bundle'),
            FieldPanel('brand'),
            FieldPanel('category'),
            FieldPanel('type'),
            FieldPanel('parent')
        ], heading='Organisation'),
    ]

    edit_handler = ObjectList(custom_panels)

    def get_linked_meta(self):
        return LinkedMetadata(
            title='{} | What\'s on'.format(self.title),
            description=self.short_description,
            path='/whats-on/{}-{}'.format(self.slug, self.pk),
            image_resource=self.featured_image
        )

    def move_under(self, parent, user):
        if not user.has_perm('events.can_change_event'):
            return False

        if parent.pk == self.pk:
            return False

        if parent.is_top_level() and not self.has_child_events():
            self.parent = parent
            return True
        else:
            return False

    def is_top_level(self):
        return self.parent is None

    def has_child_events(self):
        return self.children.count() > 0

    def __str__(self):
        return self.title


class MSLEvent(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True
    )
    disable_sync = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    last_sync = models.DateTimeField(auto_now=True)
    has_tickets = models.BooleanField()
    org_id = models.CharField(max_length=30)
    org_name = models.CharField(max_length=255)
    title = models.TextField()
    image_url = models.URLField(max_length=2000)
    url = models.URLField(max_length=2000)
    location = models.CharField(max_length=255)
    msl_event_id = models.CharField(max_length=255)
    body_html = models.TextField()
    description = models.TextField()

    # absent here at the moment: types[], brand

    @staticmethod
    def create_from_msl(api_content):
        with transaction.atomic():
            title = api_content['Title']
            start_time = arrow.get(api_content['StartDate']).replace(tzinfo=tz.gettz('Europe/London')).datetime
            end_time = arrow.get(api_content['EndDate']).replace(tzinfo=tz.gettz('Europe/London')).datetime

            event_url = api_content['Url']

            if not api_content['HasTickets'] and event_url.startswith('https://www.sussexstudent.com/ents/event'):
                event_url = ''

            event = Event(
                title=title,
                start_time=start_time,
                end_time=end_time,
                location_display=api_content['Location'],
                short_description=api_content['Description'],
                kicker=api_content['Organisation'],
                url=event_url,
                body=api_content['Body'],
                student_group=StudentGroup.get_by_msl_id(api_content['OrganisationId']),
            )

            local_remote_image = RemoteImage.try_image(api_content['ImageUrl'])

            if local_remote_image is not None:
                event.featured_image = local_remote_image

            event.save()

            msl_event = MSLEvent(
                event=event,
                title=title,
                start_time=start_time,
                end_time=end_time,
                msl_event_id=api_content['Id'],
                has_tickets=api_content['HasTickets'],
                org_id=api_content['OrganisationId'],
                org_name=api_content['Organisation'],
                image_url=api_content['ImageUrl'],
                url=api_content['Url'],
                location=api_content['Location'],
                body_html=api_content['Body'],
                description=api_content['Description'],
            )

            msl_event.save()
            return msl_event

    def update_from_msl(self, api_content):
        title = api_content['Title']
        location = api_content['Location']
        start_time = arrow.get(api_content['StartDate']).replace(tzinfo=tz.gettz('Europe/London')).datetime
        end_time = arrow.get(api_content['EndDate']).replace(tzinfo=tz.gettz('Europe/London')).datetime
        # TODO: implement change checking before saving/setting

        if not self.disable_sync:
            event_url = api_content['Url']

            if not api_content['HasTickets'] and event_url.startswith('https://www.sussexstudent.com/ents/event'):
                event_url = ''

            self.event.title = title
            self.event.start_time = start_time
            self.event.end_time = end_time
            self.event.location_display = location
            self.event.short_description = api_content['Description']
            self.event.kicker = api_content['Organisation']
            self.event.url = event_url
            self.event.body = api_content['Body']
            self.event.student_group = StudentGroup.get_by_msl_id(api_content['OrganisationId'])

            local_remote_image = RemoteImage.try_image(api_content['ImageUrl'])

            if local_remote_image is not None:
                self.event.featured_image = local_remote_image

            try:
                venue_map = AutoLocationDisplayToVenue.objects.get(location=location)
                self.event.venue = venue_map.venue
            except AutoLocationDisplayToVenue.DoesNotExist:
                self.event.venue = None

            self.event.save()

        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.msl_event_id = api_content['Id']
        self.has_tickets = api_content['HasTickets']
        self.org_id = api_content['OrganisationId']
        self.org_name = api_content['Organisation']
        self.image_url = api_content['ImageUrl']
        self.url = api_content['Url']
        self.location = api_content['Location']
        self.body_html = api_content['Body']
        self.description = api_content['Description']
        self.save()
