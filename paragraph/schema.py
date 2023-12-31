from django.utils import timezone
from django.contrib.auth import authenticate

from account.models import Account, get_default_profile_image
from account.utils import sign_up_complete, password_reset_firstflow, password_reset_secondflow
from account.forms import AccountUpdateForm, RegistrationForm, AccountAuthenticationForm, ImageUpdateForm

from notes.utils import get_note, get_my_notes, get_paragraph, get_my_paragraphs, get_paragraph_feed, create_note, update_note, delete_note, create_paragraph, delete_paragraph

from friendships.models import FriendList, FriendUtilities
from friendships.utils import isfriend, isblocked, amiblocked, persontouser, usertoperson, acceptrequest, cancelrequest, declinerequest, unfriend, unblockperson, sendrequest, blockperson, get_friend_requests, get_blocked_users, get_sent_requests

from texts.models import TextMessage

from live_mode.utils import get_now_playing_feed, set_now_playing_switch, update_now_playing, get_my_now_playing

from graph.utils import send_test_message, update_fcm_token, new_message_notification, new_request_notification

from mediashare.utils import upload_media, delete_media, get_media

import graphene
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphene_file_upload.scalars import Upload
from graphql_jwt.shortcuts import get_token, create_refresh_token


#Validation Rule
from graphql import ExecutionResult, parse, validate
from graphql.validation import NoSchemaIntrospectionCustomRule


from django.conf import settings

from .types import AccountType, FriendListType,FriendUtilitiesType ,TextMessageType, NoteType, ParagraphType, NowPlayingType, SharedMediaType, ErrorType





class ValidatingSchema(graphene.Schema):
    def __init__(self, *args, validation_rules=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_rules = validation_rules

    def execute(self, *args, **kwargs):
        return self.validate(*args, **kwargs) or super().execute(*args, **kwargs)

    async def execute_async(self, *args, **kwargs):
        return self.validate(*args, **kwargs) or await super().execute_async(*args, **kwargs)

    def validate(self, *args, **kwargs):
        if query := (kwargs.get("source") or kwargs.get("request_string")):
            errors = validate(self.graphql_schema, parse(query), rules=self.validation_rules, max_errors=3)
            if errors:
                return ExecutionResult(errors=errors)








class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()





class Query(graphene.ObjectType):

    sent_media = graphene.Field(SharedMediaType, friend_id=graphene.Int())
    def resolve_sent_media(root, info, friend_id):
        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        media_to_get = get_media(currentuser, person)
        return media_to_get
    
    received_media = graphene.Field(SharedMediaType, friend_id=graphene.Int())
    def resolve_received_media(root, info, friend_id):
        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        media_to_get = get_media(person, currentuser)
        return media_to_get

    me = graphene.Field(AccountType)
    def resolve_me(root, info):
        # Querying a list
        user = info.context.user
        return user

    now_playing_switch_status = graphene.Boolean()
    def resolve_now_playing_switch_status(root, info):
        if info.context.user.is_authenticated:
            currentuser = info.context.user
            my_now_playing = get_my_now_playing(currentuser)
            now_playing_switch = my_now_playing.switch
            return now_playing_switch

    nowplayinglist = graphene.List(NowPlayingType)
    def resolve_nowplayinglist(root, info):
        user = info.context.user
        nowPlayingFeed = get_now_playing_feed(user)
        return nowPlayingFeed


    friendrequests = graphene.List(AccountType)
    def resolve_friendrequests(root, info):
        user = info.context.user
        friendrequests = get_friend_requests(user)
        return friendrequests
    
    blockedusers = graphene.List(AccountType)
    def resolve_blockedusers(root, info):
        user = info.context.user
        blockedusers = get_blocked_users(user)
        return blockedusers
    
    sentrequests = graphene.List(FriendUtilitiesType)
    def resolve_sentrequests(root, info):
        user = info.context.user
        sentrequests = get_sent_requests(user)
        return sentrequests

    note = graphene.Field(NoteType, pk=graphene.String())
    def resolve_note(root, info, pk):
        this_note = get_note(pk)
        if this_note.writer == info.context.user:
            return this_note
        

    mynotes = graphene.List(NoteType)
    def resolve_mynotes(root, info):
        me = info.context.user
        my_notes = get_my_notes(me)
        return my_notes
    
    paragraph = graphene.Field(ParagraphType, pk=graphene.String())
    def resolve_paragraph(root, info, pk):
        this_paragraph = get_paragraph(pk)
        if this_paragraph.writer == info.context.user:
            return this_paragraph
        

    myparagraphs = graphene.List(ParagraphType)
    def resolve_myparagraphs(root, info):
        me = info.context.user
        my_paragraphs = get_my_paragraphs(me)
        return my_paragraphs
    
    paragraphfeed = graphene.List(ParagraphType)
    def resolve_paragraphfeed(root, info):
        me = info.context.user
        my_feed = get_paragraph_feed(me)
        return my_feed

    account = graphene.Field(AccountType, user_id=graphene.Int())
    def resolve_account(root, info, user_id):
        # Querying a list
        account = Account.objects.get(user_id=user_id)
        return account
    
    accounts = graphene.List(AccountType)
    def resolve_accounts(root, info):
        # Querying a list
        all_accounts = Account.objects.all()
        return all_accounts

    friends = graphene.Field(FriendListType, user_id=graphene.Int())
    def resolve_friends(root, info, user_id):

        user = Account.objects.get(user_id=user_id)
        friends = FriendList.objects.get(user=user)
        return friends

    

    myfriends = graphene.Field(FriendListType)
    def resolve_myfriends(root, info):

        if info.context.user.is_authenticated:
            user = info.context.user
            my_friends = FriendList.objects.get(user=user)
            return my_friends
        
    
    userutilities = graphene.Field(FriendUtilitiesType)
    def resolve_userutilities(root, info):

        if info.context.user.is_authenticated:
            user = info.context.user
            my_utilities = FriendUtilities.objects.get(user=user)
            return my_utilities
            
    
    message = graphene.List(TextMessageType, user_id=graphene.Int())
    def resolve_message(root, info, user_id):

        if info.context.user.is_authenticated:
            user = info.context.user
            friend = Account.objects.get(user_id=user_id)
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
        

    seen = graphene.Boolean(user_id=graphene.Int())
    def resolve_seen(root, info, user_id):
        if info.context.user.is_authenticated:
            currentuser = info.context.user
            friend = Account.objects.get(user_id=user_id)
            message = TextMessage.objects.get(textreceiver=friend, textsender=currentuser)
            seenstatus = message.seen
            return seenstatus


    lastseen = graphene.String(user_id=graphene.Int())
    def resolve_lastseen(root, info, user_id):

        if info.context.user.is_authenticated:
            user = info.context.user
            friend = Account.objects.get(user_id=user_id)
            receivedmessage = TextMessage.objects.get(textreceiver=user, textsender=friend)
            seentime = timezone.localtime(receivedmessage.edittime, timezone.get_fixed_timezone(60))
            seentimeadjusted = seentime.strftime("%c")
            return seentimeadjusted
        
    profileactions = GenericScalar(user_id= graphene.Int())
    def resolve_profileactions(root, info, user_id):
        profile_relation = {}
        profile_relation["button1"] = ""
        profile_relation["button2"] = ""
        profile_relation["utilinfo"] = ""
        if info.context.user.is_authenticated:
            user = info.context.user
            other_user = Account.objects.get(user_id=user_id)
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
    
#Test Mutation
class SendTestMutation(graphene.Mutation):
    sent = graphene.Boolean()
    def mutate(root, info):
        send_test_message()
    

class updateFCMTokenMutation(graphene.Mutation):
    fcm_token = graphene.String()
    class Arguments:
        token = graphene.String(required=True)
    def mutate(root, info, token):
        user = info.context.user
        update_fcm_token(user, token)

class SendTapMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.Int(required=True)

    tap = graphene.String()
    @classmethod
    def mutate(cls, root, info, friend_id):

        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        new_message_notification(currentuser, person)

        return SendTapMutation(tap="tap tap!")


"""
Live Mode Mutations
"""
class SwitchNowPlayingMutation(graphene.Mutation):
    nowplaying = graphene.Field(NowPlayingType)
    class Arguments:
        switch = graphene.Boolean(required=True)
    def mutate(root, info, switch):
        user = info.context.user
        set_now_playing_switch(user, switch)

class UpdateNowPlayingMutation(graphene.Mutation):
    nowplaying = graphene.Field(NowPlayingType)
    class Arguments:
        playing = graphene.Boolean(required=True)
        title = graphene.String(required=True)
        artist = graphene.String()
        album = graphene.String()
        progress = graphene.Decimal(required=True)
    def mutate(root, info, playing, title, artist, album, progress):
        user = info.context.user
        update_now_playing(user, playing, title, artist, album, progress)



"""
Note Mutations
"""    
class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
    note = graphene.Field(NoteType)
    def mutate(root, info, title, body):
        writer = info.context.user
        new_note = create_note(writer, title, body)
        return CreateNoteMutation(note=new_note)
    
class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)
    note = graphene.Field(NoteType)
    def mutate(root, info, pk, title, body):
        updated_note = update_note(pk, title, body)
        return UpdateNoteMutation(note=updated_note)
    
class DeleteNoteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
    note = graphene.Field(NoteType)
    def mutate(root, info, pk):
        deleted_note = delete_note(pk)
        return DeleteNoteMutation()
    
"""
Paragraph Mutations
""" 
class CreateParagraphMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
    paragraph = graphene.Field(ParagraphType)
    def mutate(root, info, title, body):
        writer = info.context.user
        new_paragraph = create_paragraph(writer, title, body)
        return CreateParagraphMutation(paragraph=new_paragraph)

class DeleteParagraphMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
    paragraph = graphene.Field(ParagraphType)
    def mutate(root, info, pk):
        deleted_paragraph = delete_paragraph(pk)
        return DeleteParagraphMutation()    


class SendMediaMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.Int(required=True)
        media = Upload(required=True)

    media = graphene.Field(SharedMediaType)
    @classmethod
    def mutate(cls, root, info, friend_id, media=None):

        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        if media:
            upload_media(currentuser, person, media)

class DeleteMediaMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.Int(required=True)

    media = graphene.Field(SharedMediaType)
    @classmethod
    def mutate(cls, root, info, friend_id):

        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        delete_media(currentuser, person)



class SendMessageMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    message = graphene.Field(TextMessageType)
    @classmethod
    def mutate(cls, root, info, friend_id, body):

        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        message = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
        message.body = body
        message.seen = False
        message.save(update_fields=['body', 'seen', 'edittime'])

        return SendMessageMutation(message=message)

class SeenMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.Int(required=True)
    
    message = graphene.Field(TextMessageType)
    @classmethod
    def mutate(cls, root, info, friend_id):
        currentuser = info.context.user
        person = Account.objects.get(user_id=friend_id)
        message = TextMessage.objects.get(textsender=person, textreceiver=currentuser)
        sentmessage = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
        message.seen = True
        message.save(update_fields=['seen'])
        sentmessage.save(update_fields=['edittime'])

        return SeenMutation(message=message)
    
    
class ProfileActionMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        action = graphene.String(required=True)
    
    user = graphene.Field(AccountType)
    @classmethod
    def mutate(cls, root, info, user_id, action):
        currentuser = info.context.user
        person = Account.objects.get(user_id=user_id)
        
        if (action == "block"):
            blockperson(currentuser, person)
        elif (action == "add"):
            sendrequest(currentuser, person)
            new_request_notification(currentuser, person)
        elif (action == "unblock"):
            unblockperson(currentuser, person)
        elif (action == "unfriend"):
            unfriend(currentuser, person)
        elif (action == "decline"):
            declinerequest(currentuser, person)
        elif (action == "accept"):
            acceptrequest(currentuser, person)
        elif (action == "cancel"):
            cancelrequest(currentuser, person)

        return ProfileActionMutation(user=person)
    
class UpdateAccountMutation(graphene.Mutation):
    user = graphene.Field(AccountType)
    form = AccountUpdateForm
    success = graphene.Boolean()
    errors = graphene.JSONString()

    class Arguments:
        username = graphene.String(required=True)
        hide_email = graphene.Boolean(required=False)
        tagline = graphene.String(required=False)
        bio = graphene.String(required=False)
        profile_link1_text = graphene.String(required=False)
        profile_link1 = graphene.String(required=False)
        profile_link2_text = graphene.String(required=False)
        profile_link2 = graphene.String(required=False)

    def mutate(self, info, **data) -> "UpdateAccountMutation":
        

        form_to_mutate = UpdateAccountMutation.form(data, instance=info.context.user)
        if form_to_mutate.is_valid():
            form_to_mutate.save()
            return UpdateAccountMutation(success=True)
        else:
            return UpdateAccountMutation( 
                success=False, errors=form_to_mutate.errors.get_json_data()
            )
        
class RemoveProfileImageMutation(graphene.Mutation):
    user = graphene.Field(AccountType)
    def mutate(self, info):
        user = info.context.user
        user.profile_image = "/paragraph/default_profile_image.png"
        user.save(update_fields=['profile_image'])


class UpdateProfileImageMutation(graphene.Mutation):
    user = graphene.Field(AccountType)
    form = ImageUpdateForm
    success = graphene.Boolean()
    errors = graphene.JSONString()

    class Arguments:
        profile_image = Upload(required=True)

    def mutate(self, info, profile_image=None):
        if profile_image:
            user = info.context.user
            user.profile_image = profile_image
            user.save(update_fields=['profile_image'])
            return UpdateProfileImageMutation(success=True)
        else:
            return UpdateProfileImageMutation(
                success=False
            )



class RegisterMutation(graphene.Mutation):
    user = graphene.Field(AccountType)
    form = RegistrationForm
    success = graphene.Boolean()
    errors = graphene.Field(ErrorType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, **data):
       

        form_to_mutate = RegisterMutation.form(data)
        if form_to_mutate.is_valid():
            sign_up_complete(info.context, form_to_mutate)
            return RegisterMutation(success=True)
        else:
            return RegisterMutation( 
                success=False, errors=form_to_mutate.errors.get_json_data()
            )

class RequestPasswordTokenMutation(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        email = graphene.String(required=True)
    def mutate(self, info, email):
        password_reset_firstflow(email)
        return RequestPasswordTokenMutation(success=True)
    
class ResetPasswordMutation(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    class Arguments:
        token = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
    def mutate(self, info, token, password1, password2):
        if password1 != password2:
            success = False
            message = "Passwords do not match"
            return ResetPasswordMutation(success=success, message=message)
        else:
            success, message = password_reset_secondflow(token, password1)
            return ResetPasswordMutation(success=success, message=message)


class Mutation(graphene.ObjectType):

    revoke_token = graphql_jwt.relay.Revoke.Field()
    send_message = SendMessageMutation.Field()
    set_seen = SeenMutation.Field()
    profile_action = ProfileActionMutation.Field()
    account_update = UpdateAccountMutation.Field()
    note_create = CreateNoteMutation.Field()
    note_update = UpdateNoteMutation.Field()
    note_delete = DeleteNoteMutation.Field()
    paragraph_create = CreateParagraphMutation.Field()
    paragraph_delete = DeleteParagraphMutation.Field()
    login = AuthMutation.token_auth
    register = RegisterMutation.Field()
    refresh_token = AuthMutation.refresh_token
    now_playing_update = UpdateNowPlayingMutation.Field()
    now_playing_switch = SwitchNowPlayingMutation.Field()
    remove_profile_image = RemoveProfileImageMutation.Field()
    update_profile_image = UpdateProfileImageMutation.Field()
    update_fcm = updateFCMTokenMutation.Field()
    tap_user = SendTapMutation.Field()
    send_media = SendMediaMutation.Field()
    delete_sent_media = DeleteMediaMutation.Field()
    send_test_notification = SendTestMutation.Field()
    request_password_token = RequestPasswordTokenMutation.Field()
    reset_password = ResetPasswordMutation.Field()
    pass





schema = ValidatingSchema(
    query=Query,
    mutation=Mutation,
    validation_rules=(
        *filter(None, (NoSchemaIntrospectionCustomRule if not settings.DEBUG else None,)), #not 
    ),
)