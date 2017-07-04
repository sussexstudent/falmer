import arrow
from django.db import models

from falmer.matte.models import MatteImage, RemoteImage


class Venue(models.Model):
    name = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class AutoLocationDisplayToVenue(models.Model):
    venue = models.ForeignKey(Venue, null=False)
    location = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.location


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    featured_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)
    url = models.URLField(blank=True, default='')
    social_facebook = models.URLField(blank=True, default='')
    kicker = models.CharField(max_length=255, default='')
    location_display = models.CharField(max_length=255, default='')

    venue = models.ForeignKey(Venue, blank=True, null=True)
    short_description = models.TextField(default='')


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
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    url = models.URLField()
    location = models.CharField(max_length=255)
    msl_event_id = models.CharField(max_length=255)
    body_html = models.TextField()
    description = models.TextField()

    # absent here at the moment: types[], brand

    @staticmethod
    def create_from_msl(api_content):
        title = api_content['Title']
        start_time = arrow.get(api_content['StartDate']).datetime
        end_time = arrow.get(api_content['EndDate']).datetime
        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location_display=api_content['Location'],
            short_description=api_content['Description'],
            kicker=api_content['Organisation'],
            url=api_content['Url'],
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
        start_time = arrow.get(api_content['StartDate']).datetime
        end_time = arrow.get(api_content['EndDate']).datetime
        # TODO: implement change checking before saving/setting

        if not self.disable_sync:
            self.event.title = title
            self.event.start_time = start_time
            self.event.end_time = end_time
            self.event.location_display = location
            self.event.short_description = api_content['Description']
            self.event.kicker = api_content['Organisation']
            self.event.url = api_content['Url']

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
