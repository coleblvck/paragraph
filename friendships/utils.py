from friendships.models import FriendList, FriendUtilities
from texts.models import TextMessage







def sendrequest(sender, reciever):
    recieverrequests = FriendUtilities.objects.get(user=reciever)
    recieverrequests.requests.add(sender)



def cancelrequest(sender, reciever):
    recieverrequests = FriendUtilities.objects.get(user=reciever)
    recieverrequests.requests.remove(sender)



def acceptrequest(adder, addee):

    adderutilitylist = FriendUtilities.objects.get(user=adder)
    adderfriendlist = FriendList.objects.get(user=adder)
    addeefriendlist = FriendList.objects.get(user=addee)


    if addee in adderutilitylist.requests.all():
        adderfriendlist.friends.add(addee)
        addeefriendlist.friends.add(adder)
        adderutilitylist.requests.remove(addee)
        TextMessage.objects.create(textsender=adder, textreceiver=addee)
        TextMessage.objects.create(textsender=addee, textreceiver=adder)



def declinerequest(decliner, declinee):
    declinerutilitylist = FriendUtilities.objects.get(user=decliner)
    if  declinee in declinerutilitylist.requests.all():
        declinerutilitylist.requests.remove(declinee)




def unfriend(remover, removee):

    # Remove removee from remover's friend list
    removerfriendslist = FriendList.objects.get(user=remover)
    removerfriendslist.friends.remove(removee)

    # Remove remover from removee's friend list
    removeefriendslist = FriendList.objects.get(user=removee)
    removeefriendslist.friends.remove(remover)
    TextMessage.objects.filter(textsender=remover, textreceiver=removee).delete()
    TextMessage.objects.filter(textsender=removee, textreceiver=remover).delete()


def blockperson(user, person):
    userutilitylist = FriendUtilities.objects.get(user=user)
    userutilitylist.userblocked.add(person)
    if isfriend(user, person):
        unfriend(user, person)
    TextMessage.objects.filter(textsender=user, textreceiver=person).delete()
    TextMessage.objects.filter(textsender=person, textreceiver=user).delete()


def unblockperson(user, person):
    userutilitylist = FriendUtilities.objects.get(user=user)
    userutilitylist.userblocked.remove(person)





def isfriend(user, friend):

    userfriendlist = FriendList.objects.get(user=user)

    if friend in userfriendlist.friends.all():
        return True
    return False




def persontouser(user, them):
    userutilitylist = FriendUtilities.objects.get(user=user)
    if them in userutilitylist.requests.all():
        return True
    return False


def usertoperson(user, them):
    theirutilitylist = FriendUtilities.objects.get(user=them)
    if user in theirutilitylist.requests.all():
        return True
    return False




def isblocked(user, person):
    userutilitylist = FriendUtilities.objects.get(user=user)
    if person in userutilitylist.userblocked.all():
        return True
    return False

def amiblocked(user, person):
    personutilitylist = FriendUtilities.objects.get(user=person)
    if user in personutilitylist.userblocked.all():
        return True
    return False


def get_user_friend_list(user):

    user_friend_list = FriendList.objects.get(user=user).friends.all()

    return user_friend_list

def get_friend_requests(user):
    userutil = FriendUtilities.objects.get(user=user)
    friendrequests = userutil.requests.all()
    return friendrequests

def get_blocked_users(user):
    userutil = FriendUtilities.objects.get(user=user)
    blockedusers = userutil.userblocked.all()
    return blockedusers


def get_sent_requests(me):
    my_sent_requests = FriendUtilities.objects.filter(requests=me).all().only("user")

    return my_sent_requests