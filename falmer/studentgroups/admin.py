from django.contrib import admin
from django.contrib.admin import register

from .models import StudentGroup, MSLStudentGroup, MSLStudentGroupCategory


@register(StudentGroup)
class StudentGroupModelAdmin(admin.ModelAdmin):
    pass


@register(MSLStudentGroup)
class MSLStudentGroupModelAdmin(admin.ModelAdmin):
    list_select_related = ('group', )


@register(MSLStudentGroupCategory)
class MSLStudentGroupCategoryModelAdmin(admin.ModelAdmin):
    pass
