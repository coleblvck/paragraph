from django.shortcuts import render
from friendships.models import FriendUtilities

# Create your views here.


def friendsrequestsview(request, *args, **kwargs):
    context = {}

    userutil = FriendUtilities.objects.get(user=request.user)
    friendrequests = userutil.requests.all()
    context['requests'] = friendrequests


    return render(request, "friendships/requests.html", context)