from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

# create new user with graphql Mutation
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_passwork(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# query individual user based on their id
