from .models import Note, Paragraph
from friendships.utils import get_user_friend_list
from django.db.models import Q


"""
Note Methods
"""
def create_note(writer, title, body):
    new_note = Note.objects.create(writer=writer, title=title, body=body)
    return new_note

def update_note(pk, title, body):
    note_to_update = Note.objects.get(pk=pk)
    if note_to_update:
        note_to_update.title = title
        note_to_update.body = body
        note_to_update.save(update_fields=['title', 'body', 'edittime'])
        return note_to_update

def delete_note(pk):
    note_to_delete = Note.objects.get(pk=pk)
    note_to_delete.delete()


"""
Note Get Methods
"""

def get_my_notes(me):
    my_notes = Note.objects.filter(writer=me).order_by('-edittime')
    return my_notes

def get_note(pk):
    note_to_get = Note.objects.get(pk=pk)
    return note_to_get

"""
Paragraph Methods
"""

def create_paragraph(writer, title, body):
    new_paragraph = Paragraph.objects.create(writer=writer, title=title, body=body)
    return new_paragraph

def delete_paragraph(pk):
    paragraph_to_delete = Paragraph.objects.get(pk=pk)
    paragraph_to_delete.delete()


"""
Paragraph Get Methods
"""

def get_my_paragraphs(me):
    my_paragraphs = Paragraph.objects.filter(writer=me).order_by('-edittime')
    return my_paragraphs

def get_paragraph(pk):
    paragraph_to_get = Paragraph.objects.get(pk=pk)
    return paragraph_to_get

def get_my_paragraph_feed(me):
    my_friend_list = get_user_friend_list(me)
    my_feed_filter = Q()
    for friend in my_friend_list:
        my_feed_filter = my_feed_filter | Q(writer=friend)
    my_feed = Paragraph.objects.filter(my_feed_filter).order_by('-edittime')

    return my_feed