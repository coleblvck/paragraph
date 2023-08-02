from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .models import Account
from .utils import sign_up_complete

from django.conf import settings

from friendships.models import FriendList, FriendUtilities
from friendships.utils import isfriend, amiblocked, isblocked, persontouser, usertoperson, sendrequest, cancelrequest, acceptrequest, declinerequest, unfriend, blockperson, unblockperson
from django.http import JsonResponse
from account.utils import userList, searchusers


# Create your views here.


def registerview(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.username}.")

    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            sign_up_complete(request, form)


        else:
            context['registration_form'] = form



    return render(request, "account/register.html", context)


def logoutview(request):
        logout(request)
        return redirect("home")



def loginview(request):

    context = {}

    user = request.user
    if user.is_authenticated:
         return redirect("home")
    
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context['login_form'] = form
        
    return render(request, 'account/login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
         if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    
    return redirect




@never_cache
def profileview(request, *args, **kwargs):
    context = {}
    usernameentry = kwargs.get("username")
    username = usernameentry.lower()
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return HttpResponse("That user does not exist")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
        context['bio'] = account.bio
        context['profile_link1_text'] = account.profile_link1_text
        context['profile_link1'] = account.profile_link1
        context['profile_link2_text'] = account.profile_link2_text
        context['profile_link2'] = account.profile_link2


        is_self = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False

        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL


        # FriendUtil related checks
        if request.user.is_authenticated and not is_self:
            is_friend = isfriend(user, account)
            is_blocked = isblocked(user, account)
            am_iblocked = amiblocked(user, account)
            themtouser = persontouser(user, account)
            usertothem = usertoperson(user, account)
            if not am_iblocked:
                if is_friend:
                    context['button1'] = "block"
                    context['button2'] = "unfriend"
                    context['utilinfo'] = "Friends"
                elif is_blocked:
                    context['button1'] = "unblock"
                elif themtouser:
                    context['button1'] = "decline"
                    context['button2'] = "accept"
                elif usertothem:
                    context['button1'] = "cancel"
                else:
                    context['button1'] = "block"
                    context['button2'] = "add"
            else:
                if is_blocked:
                    context['button1'] = 'unblock'
                else:
                    context['button1'] = 'block'
                
                context['utilinfo'] = "You have been blocked by this user"

            if request.POST:
                if "add" in request.POST:
                    sendrequest(user, account)
                    return redirect("user:view", username=account.username)
                elif "block" in request.POST:
                    blockperson(user, account)
                    return redirect("user:view", username=account.username)
                elif "cancel" in request.POST:
                    cancelrequest(user, account)
                    return redirect("user:view", username=account.username)
                elif "unfriend" in request.POST:
                    unfriend(user, account)
                    return redirect("user:view", username=account.username)
                elif "unblock" in request.POST:
                    unblockperson(user, account)
                    return redirect("user:view", username=account.username)
                elif "decline" in request.POST:
                    declinerequest(user, account)
                    return redirect("user:view", username=account.username)
                elif 'accept' in request.POST:
                    acceptrequest(user, account)
                    return redirect("user:view", username=account.username)
                

            

        return render(request, "account/profile.html", context)
    


@login_required(login_url='/login')
def profileupdate(request, *args, **kwargs):
    account = Account.objects.get(username=request.user.username)
    context = {}    
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user:view", username=request.user.username)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                initial={
                    "id": account.id,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                    "bio": account.bio,
                    "profile_link1_text": account.profile_link1_text,
                    "profile_link1": account.profile_link1,
                    "profile_link2_text": account.profile_link2_text,
                    "profile_link2": account.profile_link2,
                }
            )
            context['form'] = form
            
    else:
        form = AccountUpdateForm(instance=request.user,
            initial={
                "id": account.id,
                "email": account.email,
                "username": account.username,
                "profile_image": account.profile_image,
                "hide_email": account.hide_email,
                "bio": account.bio,
                "profile_link1_text": account.profile_link1_text,
                "profile_link1": account.profile_link1,
                "profile_link2_text": account.profile_link2_text,
                "profile_link2": account.profile_link2,
            }
        )
        
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/updateprofile.html", context)



def userquery(request):
    context = {}
    context["allusers"] = userList()   

    return JsonResponse(context, safe=False)


def usersearch(request, username):
    context = {}
    context["matchingusers"] = searchusers(username)   

    return JsonResponse(context, safe=False)