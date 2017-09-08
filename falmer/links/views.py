from django.shortcuts import render, get_object_or_404
from django.views import generic

from falmer.events.models import Event
from falmer.studentgroups.models import StudentGroup

MODEL_MAP = {
    'e': Event,
}


class LinkRenderer(generic.DetailView):
    template_name = 'links/link_page.html'

    def get_object(self, queryset=None):
        model_key = self.kwargs['model']
        if model_key in MODEL_MAP:
            return get_object_or_404(MODEL_MAP[model_key], pk=self.kwargs['pk'])
