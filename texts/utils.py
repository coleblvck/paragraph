from texts.models import TextMessage
from django.utils import timezone




def getuserinbox(user):

    userrecievedmessages = TextMessage.objects.filter(textreceiver=user).order_by('-edittime')
    messages = []
    for message in userrecievedmessages:
        messagetime = timezone.localtime(message.edittime, timezone.get_fixed_timezone(60))
        currentmessage = [
            message.textsender.username, 
            message.body, 
            messagetime.strftime("%c"), 
            message.seen
            ]
        messages.append(currentmessage)
    return(messages)