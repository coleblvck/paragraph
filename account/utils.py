from account.models import Account, utils_on_signup
from verify_email.email_handler import send_verification_email

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



def all_users():
    accounts = Account.objects.all()
    return accounts


def sign_up_complete(request, form):
    inactive_user = send_verification_email(request=request, form=form)
    utils_on_signup(inactive_user)