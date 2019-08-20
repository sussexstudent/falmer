# Generated by Django 2.2.3 on 2019-08-20 12:56

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_auto_20190820_1356'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('content', '0055_auto_20190808_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficerEventsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.core.fields.RichTextField()),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.Curator')),
            ],
            options={
                'abstract': False,
            },
            bases=('content.page',),
        ),
    ]
