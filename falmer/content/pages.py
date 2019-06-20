from time import time

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import redirect, get_object_or_404
from wagtail.admin.views.pages import PreviewOnEdit

from falmer.content.models import PreviewData
from falmer.content.models.core import Page

# we're overriding some wagtail views made for previews here
class PreviewOnEditRemix(PreviewOnEdit):
    json_preview_session_key = 'json-preview-token'

    # here we get the PreviewData.token
    # and forward it to the client site as a query param
    def get(self, request, *args, **kwargs):
        if not settings.MSL_SITE_HOST:
            return HttpResponse('MSL_SITE_HOST not set in settings')

        page = self.get_page()

        post_data, timestamp = self.request.session.get(self.session_key,
                                                        (None, None))
        if not isinstance(post_data, str):
            post_data = ''
        form = self.get_form(page, QueryDict(post_data))

        if not form.is_valid():
            return self.error_response(page)

        token, exp = self.request.session.get(self.json_preview_session_key,
                                 (None, None))

        return redirect(f'{settings.MSL_SITE_HOST}{page.public_path}?preview={token}')

    # this post would normally save the page content to the session
    # and then the get request would render it
    # here, we also store the page data in to a model called PreviewData
    # as our content site doesn't have access to the users django session
    # we save the PreviewData.token to their session to use in the get request above
    def post(self, request, *args, **kwargs):
        # TODO: Handle request.FILES.
        preview = PreviewData.preview_edit(page_id=self.args[0], page_data=request.POST.urlencode())
        request.session[self.json_preview_session_key] = preview.token, time()
        request.session[self.session_key] = request.POST.urlencode(), time()
        form = self.get_form(self.get_page(), request.POST)
        response = {'is_valid': form.is_valid() }
        return JsonResponse(response)


def view_draft(request, page_id):
    page = get_object_or_404(Page, id=page_id).get_latest_revision_as_page()
    perms = page.permissions_for_user(request.user)
    if not (perms.can_publish() or perms.can_edit()):
        raise PermissionDenied

    preview = PreviewData.preview_draft(page_id)

    return page.serve_preview_api(preview.token, page.default_preview_mode)

