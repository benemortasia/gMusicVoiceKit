#!/usr/bin/env python
from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import re
import os.path

# import vlc

gpm = Mobileclient()
# Login with username, password, and MAC.
# MAC helps Google Play Services identify the device
gpm.login('jpage628@gmail.com', pw, Mobileclient.FROM_MAC_ADDRESS)
# User note: always 'escape' the backslashes, or we may get special characters
# 'D:\testfolder' would translate the \t into a tab, for example:
# 'D:    estfolder'
song_location = 'D:\\Users\\JP\\Dump\\'


def play_song(song="Raindrop"):
    if Mobileclient.is_authenticated(gpm):
        mm = Musicmanager()
        # mm.perform_oauth('C:\Users\JP\Python\oauth.cred')
        mm.login('C:\\Users\\JP\\Python\\oauth.cred')
        if Musicmanager.is_authenticated(mm):
            song_dict = mm.get_purchased_songs()
            song_pattern = re.compile(r'(?:.)*\s?(' + re.escape(song) + r')\s?(?:.)*', re.IGNORECASE)
            
            for song in song_dict:
                m = re.match(song_pattern, song['title'])
                print m
                print song_dict.pop()
                
                if re.match(song_pattern, song['title']) is not None:
                    print 'Song found!'
                    song_id = song['id']
                    filename, audio = mm.download_song(song_id)
                    
                    # check if song is already downloaded
                    try:
                        print song_location + filename
                        if os.path.isfile(song_location + filename):
                            print 'Song is already downloaded...'
                            print 'Playing song.'
                            break
                        else:
                            with open(song_location + filename, 'wb') as f:
                                f.write(audio)
                    except (OSError, IOError):
                        print 'An error has occurred.'
                        break

                    # TODO
                    # vlc.MediaPlayer.play(filename)
                else:
                    print 'Song not found.'
            print song_dict.pop()
        else:
            print 'Looks like you need to authenticate.'
            mm.perform_oauth('C:\\Users\\JP\\Python\\oauth.cred')

        Mobileclient.logout(gpm)
        mm.logout()
    else:
        print 'Mobileclient is not authenticated.'


play_song()
