from falmer.content.models.core import ClickThrough
from .staff import StaffPage, StaffMemberSnippet
from .section_content import SectionContentPage
from .selection_grid import SelectionGridPage
from .officer_overview import OfficerOverviewPage
from .homepage import HomePage
from .freshers import FreshersHomepage
from .generic import KBRootPage, KBCategoryPage, AnswerPage, ReferencePage, DetailedGuidePage, DetailedGuideSectionPage
from .basic import StubPage, BasicContentPage
from .outlets import OutletIndexPage, OutletPage


all_pages = (
    StaffPage,
    StaffMemberSnippet,

    SectionContentPage,

    SelectionGridPage,

    OfficerOverviewPage,

    HomePage,

    KBRootPage,
    KBCategoryPage,
    AnswerPage,
    ReferencePage,
    DetailedGuidePage,
    DetailedGuideSectionPage,

    StubPage,
    BasicContentPage,

    OutletIndexPage,
    OutletPage,

    FreshersHomepage,

    ClickThrough,
)


name_to_class_map = {cls.__name__: cls for cls in all_pages}
