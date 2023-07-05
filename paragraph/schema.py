from account.models import Account
from friendships.models import FriendList, FriendUtilities
from texts.models import TextMessage
from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
import graphql_jwt

from friendships import utils



class AccountType(DjangoObjectType):
    class Meta:
        model = Account
        fields = ("email", "username", "date_joined", "profile_image", "bio", "profile_link1_text", "profile_link1", "profile_link2_text", "profile_link2", "hide_email")


class FriendListType(DjangoObjectType):
    class Meta:
        model = FriendList
        fields = ("user", "friends")


class FriendUtilitiesType(DjangoObjectType):
    class Meta:
        model = FriendUtilities
        fields = ("user", "requests", "userblocked")


class TextMessageType(DjangoObjectType):
    class Meta:
        model = TextMessage
        fields = ("textsender", "textreceiver", "body", "edittime", "seen")



class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    refresh_token = mutations.RefreshToken.Field()





class Query(UserQuery, MeQuery, graphene.ObjectType):
    accounts = graphene.Field(AccountType, username=graphene.String())
    def resolve_accounts(root, info, username):
        # Querying a list
        return Account.objects.get(username=username)

    friends = graphene.Field(FriendListType, username=graphene.String())
    def resolve_friends(root, info, username):

        user = Account.objects.get(username=username)
        return FriendList.objects.get(user=user)

    

    myfriends = graphene.Field(FriendListType)
    def resolve_myfriends(root, info):

        if info.context.user.is_authenticated:
            user = info.context.user
            return FriendList.objects.get(user=user)
        
    
    userutilities = graphene.Field(FriendUtilitiesType)
    def resolve_userutilities(root, info):

        if info.context.user.is_authenticated:
            user = info.context.user
            return FriendUtilities.objects.get(user=user)
            
    
    message = graphene.List(TextMessageType, otheruser=graphene.String())
    def resolve_message(root, info, otheruser):

        if info.context.user.is_authenticated:
            user = info.context.user
            friend = Account.objects.get(username=otheruser)
            sentmessage = TextMessage.objects.get(textreceiver=friend, textsender=user)
            receivedmessage = TextMessage.objects.get(textreceiver=user, textsender=friend)
            context = [receivedmessage, sentmessage]
            return context


    mymessages = graphene.List(TextMessageType)
    def resolve_mymessages(root, info):

        if info.context.user.is_authenticated:
            user = info.context.user
            userrecievedmessages = TextMessage.objects.filter(textreceiver=user).order_by('-edittime')
            return userrecievedmessages
        

    seen = graphene.Boolean(otheruser=graphene.String())
    def resolve_seen(root, info, otheruser):
        if info.context.user.is_authenticated:
            currentuser = info.context.user
            friend = Account.objects.get(username=otheruser)
            message = TextMessage.objects.get(textreceiver=friend, textsender=currentuser)
            seenstatus = message.seen
            return seenstatus


    lastseen = graphene.String(otheruser=graphene.String())
    def resolve_lastseen(root, info, otheruser):

        if info.context.user.is_authenticated:
            user = info.context.user
            friend = Account.objects.get(username=otheruser)
            receivedmessage = TextMessage.objects.get(textreceiver=user, textsender=friend)
            seentime = timezone.localtime(receivedmessage.edittime, timezone.get_fixed_timezone(60))
            seentimeadjusted = seentime.strftime("%c")
            return seentimeadjusted


class SendMessageMutation(graphene.Mutation):
    class Arguments:
        friend = graphene.String(required=True)
        body = graphene.String(required=True)

    message = graphene.Field(TextMessageType)
    @classmethod
    def mutate(cls, root, info, friend, body):

        currentuser = info.context.user
        person = Account.objects.get(username=friend)
        message = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
        message.body = body
        message.seen = False
        message.save(update_fields=['body', 'seen', 'edittime'])

        return SendMessageMutation(message=message)

class SeenMutation(graphene.Mutation):
    class Arguments:
        friend = graphene.String(required=True)
    
    message = graphene.Field(TextMessageType)
    @classmethod
    def mutate(cls, root, info, friend):
        currentuser = info.context.user
        person = Account.objects.get(username=friend)
        message = TextMessage.objects.get(textsender=person, textreceiver=currentuser)
        sentmessage = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
        message.seen = True
        message.save(update_fields=['seen'])
        sentmessage.save(update_fields=['edittime'])

        return SeenMutation(message=message)

class Mutation(AuthMutation, graphene.ObjectType):

    revoke_token = graphql_jwt.Revoke.Field()
    send_message = SendMessageMutation.Field()
    set_seen = SeenMutation.Field()
    pass




schema = graphene.Schema(query=Query, mutation=Mutation)