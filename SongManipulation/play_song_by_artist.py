#!/usr/bin/env python
from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import re

# import vlc

gpm = Mobileclient()
# Login with username, password, and MAC.
# MAC helps Google Play Services identify the device
gpm.login('jpage628@gmail.com', '_c0mplex', Mobileclient.FROM_MAC_ADDRESS)
# User note: always 'escape' the backslashes, or we may get special characters
# 'D:\testfolder' would translate the \t into a tab, for example:
# 'D:    estfolder'
song_location = 'C:\\Users\\JP\Music\\Downloaded Music\\'


def play_song_by_artist(song="Raindrop", artist="Chopin"):
    if Mobileclient.is_authenticated(gpm):
        mm = Musicmanager()
        # mm.perform_oauth('C:\Users\JP\Python\oauth.cred')
        mm.login('C:\\Users\\JP\\Python\\oauth.cred')
        if Musicmanager.is_authenticated(mm):
            print 'MM is authenticated.'
            song_dict = mm.get_purchased_songs()

            # oh boy, here comes the Regex..
            song_pattern = re.compile(r'(?:.)*\s?(' + re.escape(song) + r')\s?(?:.)*', re.IGNORECASE)
            artist_pattern = re.compile(r'(?:.)*\s?(' + re.escape(artist) + r')\s?(?:.)*', re.IGNORECASE)

            for song in song_dict:
                m = re.match(artist_pattern, song['artist'])
                print m
                print song_dict.pop()
                if (re.match(song_pattern, song['title']) is not None and
                        re.match(artist_pattern, song['artist']) is not None):
                    print 'Song found!'
                    song_id = song['id']
                    filename, audio = mm.download_song(song_id)
                    # TODO
                    # check if song already exists in song_location, no need to download again
                    # just play
                    with open(song_location + filename, 'wb') as f:
                        f.write(audio)

                    # TODO
                    # vlc.MediaPlayer.play(filename)
                else:
                    print 'Song not found.'
        else:
            print 'Looks like you need to authenticate.'
            mm.perform_oauth('C:\\Users\\JP\\Python\\oauth.cred')

        Mobileclient.logout(gpm)
        mm.logout()
    else:
        print 'Mobile client is not authenticated.'


play_song_by_artist()
