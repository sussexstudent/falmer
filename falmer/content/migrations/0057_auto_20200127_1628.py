# Generated by Django 2.2.9 on 2020-01-27 16:28

from django.db import migrations
import falmer.content.blocks
import falmer.content.models.selection_grid
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0056_officereventspage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectiongridpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading_hero', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(help_text='Leave empty to use the page title', required=False)), ('image', falmer.content.blocks.FalmerImageChooserBlock())])), ('text', wagtail.core.blocks.StructBlock([('value', falmer.content.blocks.RichTextWithExpandedContent(features=['h2', 'h3', 'bold', 'italic', 'ol', 'ul', 'hr', 'link']))])), ('selection_grid', wagtail.core.blocks.ListBlock(falmer.content.models.selection_grid.GridItem))]),
        ),
    ]
