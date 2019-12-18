from collections import OrderedDict
from functools import partial
import six
from graphene import InputObjectType,Argument
from graphene.types.argument import to_arguments
from graphene_django.filter.utils import get_filtering_args_from_filterset, get_filterset_class
from .utils import NonNullDjangoConnectionField

def get_filtering_input_from_filterset(filterset_class, node_type):
    """ Inspect a FilterSet and produce the arguments to pass to
        a Graphene Field. These arguments will be available to
        filter against in the GraphQL
    """
    from graphene_django.forms.converter import convert_form_field

    args = {}
    for name, filter_field in six.iteritems(filterset_class.base_filters):
        field_type = convert_form_field(filter_field.field)
        field_type.description = filter_field.label
        args[name] = field_type

    return {'filter': Argument(type(f'{node_type}FilterInput', (InputObjectType, ), args)) }


class FalmerDjangoFilterConnectionField(NonNullDjangoConnectionField):

    def __init__(self, type, fields=None, order_by=None,
                 extra_filter_meta=None, filterset_class=None,
                 *args, **kwargs):
        self._fields = fields
        self._provided_filterset_class = filterset_class
        self._filterset_class = None
        self._extra_filter_meta = extra_filter_meta
        self._base_args = None
        super(FalmerDjangoFilterConnectionField, self).__init__(type, *args, **kwargs)

    @property
    def args(self):
        print(self.filtering_args)
        return to_arguments(self._base_args or OrderedDict(), self.filtering_args)

    @args.setter
    def args(self, args):
        self._base_args = args

    @property
    def filterset_class(self):
        if not self._filterset_class:
            fields = self._fields or self.node_type._meta.filter_fields
            meta = dict(model=self.model,
                        fields=fields)
            if self._extra_filter_meta:
                meta.update(self._extra_filter_meta)

            self._filterset_class = get_filterset_class(self._provided_filterset_class, **meta)

        return self._filterset_class

    @property
    def filtering_args(self):

        return get_filtering_input_from_filterset(self.filterset_class, self.node_type)

    @staticmethod
    def merge_querysets(default_queryset, queryset):
        # There could be the case where the default queryset (returned from the filterclass)
        # and the resolver queryset have some limits on it.
        # We only would be able to apply one of those, but not both
        # at the same time.

        # See related PR: https://github.com/graphql-python/graphene-django/pull/126

        assert not (default_queryset.query.low_mark and queryset.query.low_mark), (
            'Received two sliced querysets (low mark) in the connection, please slice only in one.'
        )
        assert not (default_queryset.query.high_mark and queryset.query.high_mark), (
            'Received two sliced querysets (high mark) in the connection, please slice only in one.'
        )
        low = default_queryset.query.low_mark or queryset.query.low_mark
        high = default_queryset.query.high_mark or queryset.query.high_mark
        default_queryset.query.clear_limits()
        queryset = default_queryset & queryset
        queryset.query.set_limits(low, high)
        return queryset

    @classmethod
    def connection_resolver(cls, resolver, connection, default_manager, max_limit,
                            enforce_first_or_last, filterset_class, filtering_args,
                            root, info, **args):
        filter_kwargs = {k: v for k, v in args.items() if k in ['filter']}

        qs = filterset_class(
            data=filter_kwargs['filter'] if 'filter' in filter_kwargs else {},
            queryset=default_manager.get_queryset()
        ).qs

        return super(FalmerDjangoFilterConnectionField, cls).connection_resolver(
            resolver,
            connection,
            qs,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )

    def get_resolver(self, parent_resolver):
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.type,
            self.get_manager(),
            self.max_limit,
            self.enforce_first_or_last,
            self.filterset_class,
            self.filtering_args
        )
