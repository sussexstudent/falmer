import graphene

from . import types
from . import models


class MoveEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int()
        destination_event_id = graphene.Int()

    ok = graphene.Boolean()
    event = graphene.Field(types.Event)

    def mutate(self, info, event_id, destination_event_id):
        try:
            event = models.Event.objects.get(pk=event_id)
            dest_event = models.Event.objects.get(pk=destination_event_id)

            success = event.move_under(dest_event, user=info.context.user)

            event.save()

        except models.Event.DoesNotExist:
            return MoveEvent(ok=False)

        return MoveEvent(ok=success, event=event)


class Mutations(graphene.ObjectType):
    move_event = MoveEvent.Field()
