# Generated by Django 2.0.8 on 2018-09-11 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('content', '0038_auto_20180818_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickThrough',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('target_link', models.TextField(blank=True, default='')),
                ('target_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='click_throughs', to='content.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('content.page',),
        ),
        migrations.AddField(
            model_name='kbcategorypage',
            name='page_icon',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
    ]
