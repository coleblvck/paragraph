from .models import SharedMedia

def upload_media(sender, receiver, file):
    file_object, created = SharedMedia.objects.get_or_create(mediasender=sender, mediareceiver=receiver)
    file_object.media = file
    file_object.save(update_fields=["media"])

def delete_media(sender, receiver):
    file_object, created = SharedMedia.objects.get_or_create(mediasender=sender, mediareceiver=receiver)
    file_object.media = None
    file_object.save(update_fields=["media"])

def get_media(sender, receiver):
    file_object, created = SharedMedia.objects.get_or_create(mediasender=sender, mediareceiver=receiver)
    return file_object