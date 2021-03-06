# Generated by Django 2.0.5 on 2018-07-04 10:03

from django.db import migrations
import falmer.content.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0003_auto_20180703_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='main',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.StructBlock([('value', wagtail.core.blocks.RichTextBlock(features=['h2', 'bold', 'italic', 'ol', 'ul', 'hr']))])), ('image', wagtail.core.blocks.StructBlock([('image', falmer.content.blocks.FalmerImageChooserBlock(required=True)), ('alternative_title', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('callout', wagtail.core.blocks.StructBlock([('value', wagtail.core.blocks.TextBlock()), ('variant', wagtail.core.blocks.ChoiceBlock(choices=[('info', 'Info'), ('alert', 'Alert')], label='Variant'))]))], blank=True, help_text='Any additional information about this deal'),
        ),
    ]
