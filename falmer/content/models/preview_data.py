from django.db import models
from django.contrib.postgres.fields import JSONField
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from falmer.content.models.core import Page


def get_form(page, query_dict):
    form_class = page.get_edit_handler().get_form_class()
    parent_page = page.get_parent().specific

    return form_class(query_dict, instance=page, parent_page=parent_page)

# view draft -> page id
# view preview of edit -> content,
# view preview of uncreated page -> content_type_app_name, content_type_model_name, parent_page_id + content


class PreviewData(models.Model):
    token = models.TextField()
    data = JSONField(default=dict)
    preview_method = models.CharField(choices=(('DRAFT', 'Draft'), ('EDIT', 'Edit'), ('CREATE', 'Create')), max_length=6)

    def get_preview_model(self):

        if self.preview_method == 'DRAFT':
            return get_object_or_404(Page,
                                     id=self.data['page_id']).get_latest_revision_as_page()
        elif self.preview_method == 'EDIT':
            page = get_object_or_404(Page,
                                     id=self.data['page_id']).get_latest_revision_as_page()
            form = get_form(page, QueryDict(self.data['content']))

            if not form.is_valid():
                return 'error'

            model = form.save(commit=False)

            return model
        elif self.preview_method == 'CREATE':
            pass
        else:
            return None

    @staticmethod
    def preview_draft(page_id):
        model = PreviewData(
            data={'page_id': page_id},
            preview_method='DRAFT',
            token=get_random_string(24)
        )

        model.save()

        return model

    @staticmethod
    def preview_edit(page_id, page_data):
        model = PreviewData(
            data={'content': page_data, 'page_id': page_id},
            preview_method='EDIT',
            token=get_random_string(24)
        )

        model.save()

        return model

    @staticmethod
    def preview_nonexistent_page(self):
        pass

