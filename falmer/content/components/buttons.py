from wagtail.core import blocks

from falmer.content.blocks import FalmerPageChooserBlock
from falmer.content.components.base import Component


class StartButton(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    page = FalmerPageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)


start_button = Component('start_button', StartButton)


class BasicButton(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    page = FalmerPageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)

basic_button = Component('basic_button', BasicButton)
