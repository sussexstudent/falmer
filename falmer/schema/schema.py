import importlib
from inspect import getmembers, isclass
import os
# from django.db.models import FileField
import graphene
from .converters import register_converters

register_converters()

from graphene_django import DjangoConnectionField as _DjangoConnectionField


from falmer.content.types import GenericPage, page_types_map


class DjangoConnectionField(_DjangoConnectionField):

    """
    Temporary fix for select_related issue
    """

    @classmethod
    def merge_querysets(cls, default_queryset, queryset):
        """
        This discarded all select_related and prefetch_related:
        # return default_queryset & queryset
        """
        return queryset


class File(graphene.ObjectType):
    resource = graphene.String()

    def resolve_resource(self, info):
        if self is None:
            return ''
        return self.url


class QueriesAbstract(graphene.ObjectType):
    pass


class MutationsAbstract(graphene.ObjectType):
    pass


queries_base_classes = [QueriesAbstract]
mutations_base_classes = [MutationsAbstract]

current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
current_module = current_directory.split('/')[-3]
subdirectories = [
    x
    for x in os.listdir(current_directory)
    if os.path.isdir(os.path.join(current_directory, x)) and
       x != '__pycache__'
]


for directory in subdirectories:
    try:
        module = importlib.import_module(f'{current_module}.{directory}.queries')
        if module:
            classes = [x for x in getmembers(module, isclass)]
            queries = [x[1] for x in classes if 'Query' in x[0]]
            queries_base_classes += queries
    except ModuleNotFoundError:
        pass

    try:
        module = importlib.import_module(f'{current_module}.{directory}.mutations')
        if module:
            classes = [x for x in getmembers(module, isclass)]
            mutations = [x[1] for x in classes if 'Mutations' in x[0]]
            mutations_base_classes += mutations
    except ModuleNotFoundError:
        pass

queries_base_classes = queries_base_classes[::-1]
mutations_base_classes = mutations_base_classes[::-1]

query_properties = {}
mutations_properties = {}

for base_class in queries_base_classes:
    query_properties.update(base_class.__dict__['_meta'].fields)

for base_class in mutations_base_classes:
    mutations_properties.update(base_class.__dict__['_meta'].fields)


Queries = type(
    'Queries',
    tuple(queries_base_classes),
    query_properties
)

Mutations = type(
    'Mutations',
    tuple(mutations_base_classes),
    mutations_properties
)


schema = graphene.Schema(query=Queries, types=list(page_types_map.values()) + [GenericPage], mutation=Mutations)
