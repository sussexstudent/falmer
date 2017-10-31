from django.db import models
from django_extensions.db.fields import AutoSlugField

from falmer.matte.models import MatteImage, RemoteImage


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_prospective = models.BooleanField(default=False)
    description = models.TextField(default='', blank=True)
    logo = models.ForeignKey(MatteImage, null=True, blank=True)
    link = models.CharField(default='', max_length=255, blank=True)

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
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def get_group_image_url(url):
    # this is the name of the default MSL image
    if '67fc461a61a4482cae44fb89fd670903' in url:
        return None

    return url


class MSLStudentGroup(models.Model):
    group = models.OneToOneField(StudentGroup, related_name='msl_group')

    description = models.TextField(default='')
    msl_group_id = models.IntegerField(unique=True)
    logo = models.ForeignKey(MatteImage, null=True)
    link = models.CharField(max_length=255)
    logo_url = models.TextField(default='')
    category = models.ForeignKey(MSLStudentGroupCategory)
    last_sync = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group.name

    @staticmethod
    def create_from_msl(content):
        group = StudentGroup.objects.create(
            name=content['name'],
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

        local_remote_image = RemoteImage.try_image(image)

        if local_remote_image is not None:
            msl_group.logo = local_remote_image

        msl_group.save()

        return msl_group

    def update_from_msl(self, content):
        image = get_group_image_url(content['logo_url'])

        self.msl_group_id = content['id']
        self.description = content['description']
        self.group.description = content['description']
        self.link = content['link']
        self.group.link = content['link']
        self.logo_url = image or ''
        category, created_category = MSLStudentGroupCategory.objects.get_or_create(name=content['category'])
        self.category = category

        local_remote_image = RemoteImage.try_image(image)

        if local_remote_image is not None:
            self.logo = local_remote_image
            self.group.logo = local_remote_image
        else:
            self.logo = None
            self.group.logo = None

        self.group.save()

        self.save()


class AwardAuthority(models.Model):
    name = models.CharField(max_length=128)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name


class Award(models.Model):
    authority = models.ForeignKey(AwardAuthority, blank=False, null=False)

    name = models.CharField(max_length=128)
    description = models.TextField(default='', blank=True)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name


class GroupAwarded(models.Model):
    group = models.ForeignKey(StudentGroup, blank=False, null=False)
    award = models.ForeignKey(Award, blank=False, null=False)

    year = models.IntegerField(blank=False, null=False)

    class Meta:
        unique_together = (('group', 'award', 'year'), )

    def __str__(self):
        return '{group} awarded {award}, in {year}'.format(
            group=self.group.name,
            award=self.award.name,
            year=self.year
        )
