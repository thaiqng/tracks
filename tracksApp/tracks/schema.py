# schema of tracks application
import graphene
from graphene_django import DjangoObjectType # to inherit the DjangoObjectType
from .models import Track, Like  # to tell graphene_django about the shape of the tracks data
from users.schema import UserType # for the like (see graphene docs)
from django.db.models import Q # allow more complex query by turning filters into objects so we can use logical operators on them

class TrackType(DjangoObjectType):
    class Meta:
        model = Track # tell TrackType to inherit Track model

# create like type
class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String()) # create track query to get all tracks as a checklist
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None): # resolve the query
        if search:
            filters = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search)
            )
            return Track.objects.filter(filters) # there are other ways of matching. See docs

        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

# mutation in createTrack class
class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType) # return created track on a track field

    class Arguments: # provide inner arg class
        title = graphene.String(required=True)
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description=None, url=None): # resolver function that store the var and persist it into db, return the class instance
        user = info.context.user or None # get info about the user
        # soft crash by raising exception if not authenticated
        if user.is_anonymous:
            raise Exception("Sign in to add a track!")

        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

# update track class
class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments: # provide inner arg class
        track_id = graphen.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description=None, url=None):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise Exception("Not allowed to update this track!")

        track.title = title
        track.description = description
        track.url = url
        track.save()
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise Exception("Not allowed to delete this track!")

        track.delete()
        return = DeleteTrack(track_id=track_id)

# create like class
class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Sign in to like this track!")

        track = Track.objects.get(id=track_id)
        if not track:
            raise Exception("Cannot find a track with this ID!")

        Like.objects.create(
            user=user,
            track=track
        )
        return CreateLike(user=user,track=track)

# track mutation class
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
