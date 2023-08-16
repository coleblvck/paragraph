from account.models import Account, PasswordToken, utils_on_signup
from verify_email.email_handler import send_verification_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail


def password_reset_firstflow(email):
    user = Account.objects.filter(email=email)
    if user.exists():
        #GenerateToken
        user=user[0]
        token = PasswordResetTokenGenerator().make_token(user=user)
        token_model, created = PasswordToken.objects.get_or_create(token_user=user)
        token_model.token = token
        token_model.save()
        username = user.username
        subject = "Password Reset"
        message = f"Dear {username}, your Password reset token is: {token}"
        from_email = "yourparagraph@myparagraph.space"
        to_email = email
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        

def password_reset_secondflow(token, password):
    token_model = PasswordToken.objects.filter(token=token)
    if token_model.exists():
        token_model = token_model[0]
        user = token_model.token_user
        token_validity = PasswordResetTokenGenerator().check_token(user, token)
        if token_validity:
            user.set_password(password)
            token_model.token = None
            return (True, "Success! Password set successfully")
        else:
            return (False, "Invalid Token")
    else:
        return (False, "Invalid Token")

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