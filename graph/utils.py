from .models import FCMToken, NotificationTiming
from firebase_admin.messaging import Message, Notification, send
import datetime



paragraph_logo ="https://app.myparagraph.space/media/paragraph/logos/logo_nobackground.png"
paragraph_logo_small ="https://app.myparagraph.space/media/paragraph/logos/logo_nobackground_smaller2.png"


def update_fcm_token(user, token):
    fcm_token, created = FCMToken.objects.get_or_create(user=user)
    fcm_token.token = token
    fcm_token.save()


def new_message_notification(sender, sendee):
    sender_username = sender.username
    body = f"New message from {sender_username}"
    title = "pssssttt!"


    fcm_token_object, fcm_created = FCMToken.objects.get_or_create(user=sendee)
    last_sent_timing, created = NotificationTiming.objects.get_or_create(fcm_token=fcm_token_object, sender=sender)
    registration_token = fcm_token_object.token

    if created:
        send_message(registration_token, title, body)
    
    else:
        last_sent_time = last_sent_timing.last_notify_time

        current_moment = datetime.datetime.now()
        delta = current_moment - last_sent_time
        if delta.total_seconds() > 15:
            last_sent_timing.save(update_fields=['last_notify_time'])
            send_message(registration_token, title, body)


def send_message(messagetoken, title, body):
    if messagetoken != None and messagetoken != "":
        message = Message(
            notification=Notification(title=title, body=body, image=paragraph_logo_small),
            token=messagetoken,
            )
        response = send(message)
        return('Successfully sent message:', response)
    

def send_test_message():
    message = Message(
        notification=Notification(title="This works", body="Thank God!!!!!!!!!!!!", image=paragraph_logo_small),
        token="cuiMZ8A5TPGjheZrGOW5L4:APA91bG5CAmkhiG0jVBtuxQQq1PcmReuV8lJiJwq-TyceqIh8Hanw33YyD0-WUtxL9wfrJpYrcSPypdE4VQtTCPxQQpOvUTZ4V-TIjVMvYuzLIaGPtvaMYx3o-mLreIwtH1n2dVzdNKt",
        )
    response = send(message)
    return(True)