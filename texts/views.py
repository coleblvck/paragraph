from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from texts.models import TextMessage
from friendships.models import FriendUtilities
from account.models import Account
from friendships.utils import isfriend
from django.http import JsonResponse
import json

# Create your views here.



@never_cache
@login_required(login_url='/login')
def chat(request, friend):
    context = {}
    currentuser = request.user
    account = friend.lower()
    userexists = False
    ispersonfriend = False
    person = ""
    if Account.objects.filter(username=account).exists():
        person = Account.objects.get(username=account)
        userexists = True
        ispersonfriend = isfriend(currentuser, person)
    context['person'] = person
    context['userexists'] = userexists
    context['ispersonfriend'] = ispersonfriend

    if ispersonfriend:
        inbox = TextMessage.objects.get(textsender=person, textreceiver=currentuser)
        outbox = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
        context['inbox'] = inbox
        context['outbox'] = outbox


    
        
    return render(request, "texts/chat.html", context)



@never_cache
@login_required(login_url='/login')
def textsview(request):

    context = {}
    userrecievedmessages = TextMessage.objects.filter(textreceiver=request.user).order_by('-edittime')
    context['messages'] = userrecievedmessages

    userutil = FriendUtilities.objects.get(user=request.user)
    friendrequests = userutil.requests.all()
    context['reqamount'] = len(friendrequests)
        
    return render(request, "texts/texts.html", context)


def sentmessages(request, friend):
    data = json.loads(request.body)
    messagedata = data["msg"]
    currentuser = request.user
    person = Account.objects.get(username=friend)
    sentmessage = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
    sentmessage.body = messagedata
    sentmessage.seen = False
    sentmessage.save(update_fields=['body', 'seen', 'edittime'])
    return JsonResponse("", safe=False)
    


def receivedmessages(request, friend):
    currentuser = request.user
    person = Account.objects.get(username=friend)
    receivedmessage = TextMessage.objects.get(textsender=person, textreceiver=currentuser)
    receivedmessage.seen = True
    receivedmessage.save(update_fields=['seen'])
    sentmessage = TextMessage.objects.get(textsender=currentuser, textreceiver=person)
    sentmessage.save(update_fields=['edittime'])
    messagedata = {}
    messagedata['body'] = receivedmessage.body
    messagedata['seenstatus'] = sentmessage.seen
    return JsonResponse(messagedata, safe=False)