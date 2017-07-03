from django.db import models
from falmer.matte.models import MatteImage, RemoteImage


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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

    msl_description = models.TextField(default='')
    msl_group_id = models.IntegerField(unique=True)
    msl_image = models.ForeignKey(MatteImage, null=True)
    msl_image_url = models.URLField(default='')
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
            msl_description=content['description'],
            msl_image_url=image or '',
            category=category,
        )

        local_remote_image = RemoteImage.try_image(image)

        if local_remote_image is not None:
            msl_group.msl_image = local_remote_image

        msl_group.save()

        return msl_group

    def update_from_msl(self, content):
        image = get_group_image_url(content['logo_url'])

        self.msl_group_id = content['id']
        self.msl_description = content['description']
        self.msl_image_url = image or ''
        category, created_category = MSLStudentGroupCategory.objects.get_or_create(name=content['category'])
        self.category = category

        local_remote_image = RemoteImage.try_image(image)

        if local_remote_image is not None:
            self.msl_image = local_remote_image
        else:
            self.msl_image = None

        self.save()
