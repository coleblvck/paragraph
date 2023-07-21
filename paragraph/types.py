from account.models import Account
from friendships.models import FriendList, FriendUtilities
from texts.models import TextMessage
from graphene_django import DjangoObjectType


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
