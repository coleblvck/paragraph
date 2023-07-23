from account.models import Account
from friendships.models import FriendList, FriendUtilities
from texts.models import TextMessage
from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
import graphql_jwt

from friendships.utils import isfriend, isblocked, amiblocked, persontouser, usertoperson

from .types import AccountType, FriendListType,FriendUtilitiesType ,TextMessageType






class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    refresh_token = mutations.RefreshToken.Field()





class Query(MeQuery, graphene.ObjectType):
    account = graphene.Field(AccountType, username=graphene.String())
    def resolve_account(root, info, username):
        # Querying a list
        return Account.objects.get(username=username)
    
    accounts = graphene.Field(AccountType)
    def resolve_accounts(root, info):
        # Querying a list
        return Account.objects.all()

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
        
    profileactions = graphene.String(otheruser= graphene.String())
    def resolve_profileactions(root, info, otheruser):
        profile_relation = {}
        profile_relation["button1"] = ""
        profile_relation["button2"] = ""
        if info.context.user.is_authenticated:
            user = info.context.user
            other_user = Account.objects.get(username=otheruser)
            if user != other_user:
                is_friend = isfriend(user, other_user)
                is_blocked = isblocked(user, other_user)
                am_iblocked = amiblocked(user, other_user)
                themtouser = persontouser(user, other_user)
                usertothem = usertoperson(user, other_user)
                if not am_iblocked:
                    if is_friend:
                        profile_relation['button1'] = "block"
                        profile_relation['button2'] = "unfriend"
                        profile_relation['utilinfo'] = "Friends"
                    elif is_blocked:
                        profile_relation['button1'] = "unblock"
                    elif themtouser:
                        profile_relation['button1'] = "decline"
                        profile_relation['button2'] = "accept"
                    elif usertothem:
                        profile_relation['button1'] = "cancel"
                    else:
                        profile_relation['button1'] = "block"
                        profile_relation['button2'] = "add"
                else:
                    if is_blocked:
                        profile_relation['button1'] = 'unblock'
                    else:
                        profile_relation['button1'] = 'block'
                    
                    profile_relation['utilinfo'] = "You have been blocked by this user"


        return profile_relation
    


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