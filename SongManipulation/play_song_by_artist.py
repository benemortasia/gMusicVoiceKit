#!/usr/bin/env python3

from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import re
import os
import threading

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.voicehat
from google.assistant.library.event import EventType

import vlc
import time
finish = 0

__author__ = 'Jordan Page'
__license__ = 'MIT'
__version__ = '1.0.1'

gpm = Mobileclient()

# MAC helps Google Play Services identify the device
# *** Change EXAMPLE and PASSWORD to your own Gmail login. ***

gpm.login('EXAMPLE@gmail.com', 'PASSWORD',
          Mobileclient.FROM_MAC_ADDRESS)

# If using Windows, always 'escape' the backslashes, or we may get special characters
# 'D:\testfolder' would translate the \t into a tab, for example:
# 'D:    estfolder'

song_location = '/home/pi/Music/'


def play_song_by_artist(song, artist):
    if Mobileclient.is_authenticated(gpm):
        mm = Musicmanager()
        mm.login('/home/pi/oauth.cred')

        if Musicmanager.is_authenticated(mm):
            song_dict = mm.get_purchased_songs()
            song_pattern = re.compile(r'(?:.)*\s?(' + re.escape(song)
                    + r')\s?(?:.)*', re.IGNORECASE)
            artist_pattern = re.compile(r'(?:.)*\s?(' + re.escape(artist)
                    + r')\s?(?:.)*', re.IGNORECASE)

            btn = OnButtonPress()
            btn.start()

            for song in song_dict:
                m = re.match(artist_pattern, song['artist'])
                print(m)

                if (re.match(song_pattern, song['title']) is not None and
                        re.match(artist_pattern, song['artist']) is not None):
                    print('Song found!')
                    song_id = song['id']
                    (filename, audio) = mm.download_song(song_id)

                    # get rid of non-ascii characters in file name

                    filename = filename.encode('ascii', errors='ignore')

                    # check if song is already downloaded
                    # path will look something like:
                    # /home/pi/Music/02 - Raindrop Prelude.mp3
                    # forces filename to be a string

                    filename = filename.decode('ascii')
                    path = song_location + filename
                    try:
                        if os.path.isfile(path):
                            print('Song is already downloaded...')
                            print(path)
                            print('Playing song.')

                            vlc_instance = vlc.Instance()

                            p = vlc_instance.media_player_new()
                            media = vlc_instance.media_new(path)

                            p.set_media(media)
                            events = p.event_manager()
                            events.event_attach(vlc.EventType.MediaPlayerEndReached,
                                    SongFinished)
                            p.play()
                            p.audio_set_volume(58)

                            while finish == 0:
                                duration = p.get_time() / 1000
                                (m, s) = divmod(duration, 60)

                                print('Current song is: ', path)
                                print('Length:', '%02d:%02d' % (m, s))
                                time.sleep(5)

                            p.stop()
                            break
                        else:
                            with open(path, 'wb') as f:
                                f.write(audio)
                            print('Song has been added to: ' + path)
                            print('Playing song.')

                            vlc_instance = vlc.Instance()

                            p = vlc_instance.media_player_new()
                            media = vlc_instance.media_new(path)

                            p.set_media(media)
                            events = p.event_manager()
                            events.event_attach(vlc.EventType.MediaPlayerEndReached, SongFinished)
                            p.play()
                            p.audio_set_volume(58)

                            while finish == 0:
                                duration = p.get_time() / 1000
                                m, s = divmod(duration, 60)

                                print('Current song is: ', path)
                                print('Length:', '%02d:%02d' % (m,s))
                                time.sleep(5)

                            p.stop()
                            break
                    except (OSError, IOError):
                        print('An error has occurred.')
                        break

                else:
                    print('Song not found yet.')

        else:
            print('Looks like you need to authenticate.')
            mm.perform_oauth('/home/pi/oauth.cred')

        print('Logging out.')
        Mobileclient.logout(gpm)
        mm.logout()

    else:
        print('Mobile client is not authenticated.')


class OnButtonPress(object):

    def __init__(self):
        self._task = threading.Thread(target=self._run_task)

    def start(self):
        self._task.start()

    def _run_task(self):
        print('Button press thread running...')
        credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            self._assistant = assistant
            for event in assistant.start():
                self._process_event(event)

    def _process_event(self, event):
        if event.type == EventType.ON_START_FINISHED:
            aiy.voicehat.get_button().on_press(self._on_button_pressed)

    def _on_button_pressed(_):
        print('Button was pressed.')
        global finish
        finish = 1


def SongFinished(event):
    global finish
    print('Finished playing song.')
    finish = 1


# Useful if you want to test this function independently of cloudspeech
# Replace 'Raindrop' and 'Chopin' with some other song-artist combination you may have
if __name__ == '__main__':
    play_song_by_artist('Raindrop', 'Chopin')
