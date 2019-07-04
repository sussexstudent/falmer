# Generated by Django 2.2.3 on 2019-07-04 11:20

from django.db import migrations
import falmer.content.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0050_auto_20190704_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeroverviewpage',
            name='pledges',
            field=wagtail.core.fields.StreamField([('pledge', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('body', falmer.content.blocks.RichTextWithExpandedContent(required=True)), ('image', falmer.content.blocks.FalmerImageChooserBlock()), ('status', wagtail.core.blocks.ChoiceBlock(choices=[('in_progress', 'In Progress'), ('done', 'Done'), ('blank', 'Blank')]))]))], blank=True),
        ),
    ]
