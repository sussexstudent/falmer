# Generated by Django 2.2.9 on 2020-01-27 16:28

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20190919_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='events', to='events.CategoryNode'),
        ),
        migrations.AlterField(
            model_name='event',
            name='student_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='studentgroups.StudentGroup'),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.Type'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True),
        ),
    ]