from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from falmer.content import components
from .core import Page

#
# class Outlet(Page):
#     subpage_types = ('',)
#
#     main = StreamField(
#         StreamBlock([
#             components.text.to_pair(),
#         ]), verbose_name='Main Content',
#         null=True, blank=True
#     )
#
#
# class OutletList(Page):
#     subpage_types = (Outlet,)
#
