#!/usr/bin/env python
from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import re
import os.path

import vlc

gpm = Mobileclient()
# Login with username, password, and MAC.
# MAC helps Google Play Services identify the device
gpm.login('jpage628@gmail.com', pw, Mobileclient.FROM_MAC_ADDRESS)
# User note: always 'escape' the backslashes, or we may get special characters
# 'D:\testfolder' would translate the \t into a tab, for example:
# 'D:    estfolder'
song_location = 'C:\\Users\\JP\Music\\Downloaded Music\\'


def play_song_by_artist(song="Raindrop", artist="Chopin"):
    if Mobileclient.is_authenticated(gpm):
        mm = Musicmanager()
        # mm.perform_oauth('C:\\Users\\JP\\Python\\oauth.cred')
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

                    # get rid of non-ascii characters in file name
                    filename = filename.encode('ascii', errors='ignore')

                    # check if song is already downloaded
                    # path will look something like:
                    # C:\\Users\\JP\Music\\Downloaded Music\\02 - Raindrop Prelude.mp3
                    path = song_location + filename
                    try:
                        if os.path.isfile(path):
                            print 'Song is already downloaded...'
                            print path
                            print 'Playing song.'
                            # TODO
                            # p = vlc.MediaPlayer(path)
                            # p.play()
                            break
                        else:
                            with open(path, 'wb') as f:
                                f.write(audio)
                            print 'Song has been added to: ' + path
                            print 'Playing song.'
                            # TODO
                            # p = vlc.MediaPlayer(path)
                            # p.play()
                            break
                    except (OSError, IOError):
                        print 'An error has occurred.'
                        break

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
