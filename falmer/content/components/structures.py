import re
from wagtail.core.blocks import StructBlock,CharBlock,ListBlock, BooleanBlock, RegexBlock

from falmer.content.components.base import Component

OPENING_TIME_REGEX = re.compile('[Mo|Tu|We|Th|Fr|Sa|Su|\-|,]+ [0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}')


class OpeningTimesBlock(StructBlock):
    special_tag = CharBlock(required=False, help_text='Add a little label if these are unusual opening times, for instance holidays')
    times = ListBlock(RegexBlock(OPENING_TIME_REGEX, required=True, help_text='Please see our docs for opening times formatting'))
    enabled = BooleanBlock(required=False, help_text='Disable for non-used opening times, for instance holidays')


opening_times = Component('opening_times', OpeningTimesBlock)
