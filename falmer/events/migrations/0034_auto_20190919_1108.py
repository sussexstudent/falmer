# Generated by Django 2.2.4 on 2019-09-19 10:08

from django.conf import settings
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_auto_20190820_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(blank=True, to='events.CategoryNode'),
        ),
        migrations.AlterField(
            model_name='event',
            name='curated_by',
            field=models.ManyToManyField(blank=True, through='events.EventCuration', to='events.Curator'),
        ),
        migrations.AlterField(
            model_name='event',
            name='likes',
            field=models.ManyToManyField(blank=True, through='events.EventLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='venue',
            name='website_link',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
