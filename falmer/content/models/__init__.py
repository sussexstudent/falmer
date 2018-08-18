from .staff import StaffPage, StaffDepartment, StaffSection, StaffMemberSnippet, StaffMember
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
    StaffDepartment,
    StaffSection,
    StaffMemberSnippet,
    StaffMember,

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

    FreshersHomepage
)


name_to_class_map = {cls.__name__: cls for cls in all_pages}
