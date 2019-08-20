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
        assert info.context.user.is_staff

        try:
            event = models.Event.objects.get(pk=event_id)
            dest_event = models.Event.objects.get(pk=destination_event_id)

            success = event.move_under(dest_event, user=info.context.user)

            event.save()

        except models.Event.DoesNotExist:
            return MoveEvent(ok=False)

        return MoveEvent(ok=success, event=event)



class LikeEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int()
        like_type = graphene.String()

    ok = graphene.Boolean()
    event = graphene.Field(types.Event)

    def mutate(self, info, event_id, like_type):
        assert info.context.user

        try:
            event = models.Event.objects.get(pk=event_id)
            event.like(info.context.user, like_type)

        except models.Event.DoesNotExist:
            return LikeEvent(ok=False)

        return LikeEvent(ok=True, event=event)


class Mutations(graphene.ObjectType):
    move_event = MoveEvent.Field()
    like_event = LikeEvent.Field()
