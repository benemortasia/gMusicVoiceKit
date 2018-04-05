#!/usr/bin/env python3
from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import re
import os.path
import vlc

__author__ = "Jordan Page"
__license__ = "MIT"
__version__ = "1.0.0"

gpm = Mobileclient()

# MAC helps Google Play Services identify the device
# *** Change EXAMPLE and PASSWORD to your own Gmail login. ***
gpm.login('EXAMPLE@gmail.com', 'PASSWORD', Mobileclient.FROM_MAC_ADDRESS)

# If using Windows, always 'escape' the backslashes, or we may get special characters
# 'D:\testfolder' would translate the \t into a tab, for example:
# 'D:    estfolder'
song_location = '/home/pi/Music/'


def play_song_by_artist(song="Raindrop", artist="Chopin"):
    if Mobileclient.is_authenticated(gpm):
        mm = Musicmanager()
        mm.login('/home/pi/oauth.cred')
        if Musicmanager.is_authenticated(mm):
            song_dict = mm.get_purchased_songs()

            # oh boy, here comes the Regex..
            song_pattern = re.compile(r'(?:.)*\s?(' + re.escape(song) + r')\s?(?:.)*', re.IGNORECASE)
            artist_pattern = re.compile(r'(?:.)*\s?(' + re.escape(artist) + r')\s?(?:.)*', re.IGNORECASE)

            for song in song_dict:
                m = re.match(artist_pattern, song['artist'])
                print(m)

                if (re.match(song_pattern, song['title']) is not None and
                        re.match(artist_pattern, song['artist']) is not None):
                    print('Song found!')
                    song_id = song['id']
                    filename, audio = mm.download_song(song_id)

                    # get rid of non-ascii characters in file name
                    filename = filename.encode('ascii', errors='ignore')

                    # also make sure that filename is a string
                    filename = filename.decode('ascii')
                    path = song_location + filename
                    try:
                        # check if song is already downloaded
                        # path will look something like:
                        # home/pi/Music/02 - Raindrop Prelude.mp3
                        if os.path.isfile(path):
                            print('Song is already downloaded...')
                            print(path)
                            print('Playing song.')
                            
                            p = vlc.MediaPlayer(path)
                            p.play()
                            break
                        else:
                            with open(path, 'wb') as f:
                                f.write(audio)
                            print('Song has been added to: ' + path)
                            print('Playing song.')
                            
                            p = vlc.MediaPlayer(path)
                            p.play()
                            break
                    except (OSError, IOError):
                        print('An error has occurred.')
                        break

                else:
                    print('Song not found.')
        else:
            print('Looks like you need to authenticate.')
            mm.perform_oauth('/home/pi/oauth.cred')

        Mobileclient.logout(gpm)
        mm.logout()
    else:
        print('Mobile client is not authenticated.')
        
if __name__ == '__main__':
    play_song_by_artist()
