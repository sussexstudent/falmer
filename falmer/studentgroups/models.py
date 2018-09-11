import re

from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.search import index

from falmer.matte.models import MatteImage, RemoteImage, SOURCE_GROUP_LOGO

MATCH_ORG_LINK = re.compile('/organisation/([a-z0-9_-]+)/')

AWARD_ICONS = (
    ('community', 'LeafCommunity'),
    ('development', 'LeafDevelopment'),
    ('social', 'LeafSocial'),
    ('student-voice', 'LeafStudentVoice'),
    ('team-sussex', 'LeafTeamSussex'),
    ('communications', 'LeafCommunications'),
    ('fundraising', 'LeafFundraising'),
    ('inclusivity', 'LeafInclusivity'),
)


class StudentGroup(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_prospective = models.BooleanField(default=False)
    description = models.TextField(default='', blank=True)
    logo = models.ForeignKey(MatteImage, null=True, blank=True, on_delete=models.SET_NULL)
    link = models.CharField(default='', max_length=255, blank=True)
    slug = models.CharField(default=None, max_length=255, blank=True, null=True, unique=True)

    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('description'),
        index.FilterField('last_sync'),
        index.FilterField('id'),
    ]

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_by_msl_id(cls, msl_group_id):
        try:
            msl_group = MSLStudentGroup.objects.get(msl_group_id=msl_group_id)
        except MSLStudentGroup.DoesNotExist:
            return None

        if msl_group is not None:
            return msl_group.group

        return None


class MSLStudentGroupCategory(models.Model):
    class Meta:
        verbose_name = 'MSL Student Group Category'
        verbose_name_plural = 'MSL Student Group Categories'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def get_group_image_url(url):
    # this is the name of the default MSL image
    if '67fc461a61a4482cae44fb89fd670903' in url:
        return None

    return url


def get_slug(link):
    if link:
        match = re.match(MATCH_ORG_LINK, link)
        if match:
            return match.group(1)

    return None


class MSLStudentGroup(models.Model):
    class Meta:
        verbose_name = 'MSL Student Group'
        verbose_name_plural = 'MSL Student Groups'

    group = models.OneToOneField(StudentGroup, related_name='msl_group', on_delete=models.CASCADE)

    description = models.TextField(default='')
    msl_group_id = models.IntegerField(unique=True)
    logo = models.ForeignKey(MatteImage, null=True, on_delete=models.SET_NULL)
    link = models.CharField(max_length=255)
    logo_url = models.TextField(default='')
    category = models.ForeignKey(MSLStudentGroupCategory, on_delete=models.CASCADE)
    last_sync = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group.name

    @staticmethod
    def create_from_msl(content):
        group = StudentGroup.objects.create(
            name=content['name'],
            slug=get_slug(content['link'])
        )

        category, created_category = MSLStudentGroupCategory.objects.get_or_create(name=content['category'])
        image = get_group_image_url(content['logo_url'])

        msl_group = MSLStudentGroup(
            group=group,
            msl_group_id=content['id'],
            link=content['link'],
            description=content['description'],
            logo_url=image or '',
            category=category,
        )

        local_remote_image = RemoteImage.try_image(image, SOURCE_GROUP_LOGO)

        if local_remote_image is not None:
            msl_group.logo = local_remote_image

        msl_group.save()

        return msl_group

    def update_from_msl(self, content):
        image = get_group_image_url(content['logo_url'])

        self.msl_group_id = content['id']
        self.description = content['description']
        self.group.description = content['description']
        self.group.name = content['name']
        self.group.slug = get_slug(content['link'])
        self.link = content['link']
        self.group.link = content['link']
        self.logo_url = image or ''
        category, created_category = MSLStudentGroupCategory.objects.get_or_create(name=content['category'])
        self.category = category

        local_remote_image = RemoteImage.try_image(image, SOURCE_GROUP_LOGO)

        if local_remote_image is not None:
            self.logo = local_remote_image
            self.group.logo = local_remote_image
        else:
            self.logo = None
            self.group.logo = None

        self.group.save()

        self.save()


class AwardAuthority(models.Model):
    class Meta:
        verbose_name = 'Award Authority'
        verbose_name_plural = 'Award Authorities'

    name = models.CharField(max_length=128)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name


class AwardPeriod(models.Model):
    class Meta:
        verbose_name = 'Award Period'
        verbose_name_plural = 'Award Periods'

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    authority = models.ForeignKey(AwardAuthority, blank=False, null=False, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=128)

    def __str__(self):
        return self.display_name


class Award(models.Model):
    authority = models.ForeignKey(AwardAuthority, blank=False, null=False, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    description = models.TextField(default='', blank=True)
    slug = AutoSlugField(unique=True, populate_from='name')
    link = models.URLField(blank=True, default='')
    icon = models.CharField(max_length=24, choices=AWARD_ICONS, default=AWARD_ICONS[0][0], null=False, blank=False)

    def __str__(self):
        return self.name


class GroupAwarded(models.Model):
    class Meta:
        verbose_name = 'Group Award'
        verbose_name_plural = 'Group Awards'
        unique_together = (('group', 'award', 'period', 'grade'), )

    group = models.ForeignKey(StudentGroup, blank=False, null=False, on_delete=models.CASCADE, related_name='awards')
    award = models.ForeignKey(Award, blank=False, null=False, on_delete=models.CASCADE)

    period = models.ForeignKey(AwardPeriod, blank=False, null=False, on_delete=models.CASCADE, related_name='awarded')
    grade = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return '{group} awarded {award} for {period}'.format(
            group=self.group.name,
            award=self.award.name,
            period=self.period
        )
