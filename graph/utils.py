from .models import FCMToken
from firebase_admin.messaging import Message, Notification, send



def send_message(user, title, body):
    messagetoken = FCMToken.objects.get_or_create(user=user).token
    if messagetoken != None and messagetoken != "":
        registration_token = messagetoken
        message = Message(
            notification=Notification(title=title, body=body, image="url"),
            topic="Notification from paragraph",
            token=registration_token,
            )
        response = send(message)
        return('Successfully sent message:', response)
    

def send_test_message():
    message = Message(
        notification=Notification(title="This works", body="Thank God!!!!!!!!!!!!", image=""),
        topic="Notification from paragraph",
        token="cuiMZ8A5TPGjheZrGOW5L4:APA91bG5CAmkhiG0jVBtuxQQq1PcmReuV8lJiJwq-TyceqIh8Hanw33YyD0-WUtxL9wfrJpYrcSPypdE4VQtTCPxQQpOvUTZ4V-TIjVMvYuzLIaGPtvaMYx3o-mLreIwtH1n2dVzdNKt",
        )
    response = send(message)
    return(True)