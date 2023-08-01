from friendships.utils import get_user_friend_list
from live_mode.models import NowPlaying
from django.db.models import Q
from account.models import Account


def get_now_playing_feed(me):
    my_friend_list = get_user_friend_list(me)
    my_feed_filter = Q()
    for friend in my_friend_list:
        my_feed_filter = my_feed_filter | (Q(user=friend) & Q(status=True))
    now_playing_feed = NowPlaying.objects.filter(my_feed_filter | Q(user=me)).order_by('-listentime')

    return now_playing_feed

def get_my_now_playing(me):
    my_now_playing = NowPlaying.objects.get(user=me)
    return my_now_playing

def set_now_playing_status(me, status):
    now_playing = NowPlaying.objects.get(user=me)
    now_playing.status = status
    now_playing.save(update_fields=['status'])

def update_now_playing(me, title, artist, album, progress):    
    now_playing = NowPlaying.objects.get(user=me)
    now_playing.title = title
    now_playing.artist = artist
    now_playing.album = album
    now_playing.progress = progress
    now_playing.save(update_fields=['title', 'artist', 'album', 'progress', 'listentime'])


def setupNP():
    for account in Account.objects.all():
        NowPlaying.objects.get_or_create(user=account)