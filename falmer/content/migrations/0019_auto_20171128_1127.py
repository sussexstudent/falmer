# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 11:27
from __future__ import unicode_literals

from django.db import migrations
import falmer.content.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20171017_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeroverviewpage',
            name='pledges',
            field=wagtail.wagtailcore.fields.StreamField((('pledge', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('body', falmer.content.blocks.RichTextWithExpandedContent(required=True)), ('image', falmer.content.blocks.ImageBlock()), ('status', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('in_progress', 'In Progress'), ('done', 'Done'), ('blank', 'Blank')]))))),)),
        ),
        migrations.AlterField(
            model_name='sectioncontentpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('section', wagtail.wagtailcore.blocks.StructBlock((('heading', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('body', wagtail.wagtailcore.blocks.StreamBlock((('paragraph', falmer.content.blocks.RichTextWithExpandedContent()),)))))),)),
        ),
        migrations.AlterField(
            model_name='sectioncontentpage',
            name='sidebar_body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('contact', wagtail.wagtailcore.blocks.StructBlock((('body', wagtail.wagtailcore.blocks.TextBlock()), ('name', wagtail.wagtailcore.blocks.CharBlock()), ('email', wagtail.wagtailcore.blocks.EmailBlock()))))), blank=True),
        ),
    ]