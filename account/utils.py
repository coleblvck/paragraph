from account.models import Account
from friendships.models import FriendList, FriendUtilities
from live_mode.models import NowPlaying

def userList():
    accounts = Account.objects.all()
    if accounts:
        list = []
        for account in accounts:
            eachuser = [
                account.username,
                account.profile_image.url                
                ]
            list.append(eachuser)
        return(list)
    
def searchusers(term):
    matches = []
    accounts = userList()
    for account in accounts:
        if term.lower() in account[0]:
            matches.append(account)
    return matches

def utils_on_signup(user):
    FriendList.objects.create(user=user)
    FriendUtilities.objects.create(user=user)
    NowPlaying.objects.create(user=user)

def all_users():
    accounts = Account.objects.all()
    return accounts