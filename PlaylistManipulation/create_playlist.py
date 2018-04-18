#!/usr/bin/env python3

from gmusicapi import Mobileclient

__author__ = 'Jordan Page'
__license__ = 'MIT'
__version__ = '1.0.1'

gpm = Mobileclient()

# MAC helps Google Play Services identify the device
# *** Change EXAMPLE and PASSWORD to your own Gmail login. ***
gpm.login('EXAMPLE@gmail.com', 'PASSWORD',
          Mobileclient.FROM_MAC_ADDRESS)


def create_playlist(playlist_name):

    if Mobileclient.is_authenticated(gpm):
        # the following prints all playlist names
        all_playlists = Mobileclient.get_all_playlists(gpm)
        for playlist in all_playlists:
            # print(playlist)
            temp = set()
            temp.add(playlist['name'])
            # print(temp)

        return gpm.create_playlist(playlist_name)
    else:
        print("The Mobileclient is not authenticated.")


    Mobileclient.logout(gpm)

# Useful if you want to test this function independently of cloudspeech
# Replace 'Default' with a playlist name
if __name__ == '__main__':
    create_playlist('Default')
