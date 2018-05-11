from django.contrib import admin
from django.contrib.admin import register

from .models import StudentGroup, MSLStudentGroup, MSLStudentGroupCategory, AwardPeriod, AwardAuthority, Award, GroupAwarded


@register(StudentGroup)
class StudentGroupModelAdmin(admin.ModelAdmin):
    pass


@register(MSLStudentGroup)
class MSLStudentGroupModelAdmin(admin.ModelAdmin):
    list_select_related = ('group', )


@register(MSLStudentGroupCategory)
class MSLStudentGroupCategoryModelAdmin(admin.ModelAdmin):
    pass


@register(AwardPeriod)
class AwardPeriodModelAdmin(admin.ModelAdmin):
    pass


@register(AwardAuthority)
class AwardAuthorityModelAdmin(admin.ModelAdmin):
    pass


@register(Award)
class AwardModelAdmin(admin.ModelAdmin):
    pass


@register(GroupAwarded)
class GroupAwardedModelAdmin(admin.ModelAdmin):
    pass
