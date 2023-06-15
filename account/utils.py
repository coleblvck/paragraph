from account.models import Account

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