#!/usr/bin/env python3

from gmusicapi import Mobileclient

__author__ = 'Jordan Page'
__license__ = 'MIT'
__version__ = '1.0.1'

gpm = Mobileclient()

# *** Change EXAMPLE and PASSWORD to your own Gmail login. ***
# If using the device on more than one network, you'll need an android_id
# Otherwise, you may use Mobileclient.FROM_MAC_ADDRESS as the third argument.
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
        print("Mobileclient could not authenticate.")


    Mobileclient.logout(gpm)

# Useful if you want to test this function independently of cloudspeech
# Replace 'Default' with a playlist name
if __name__ == '__main__':
    create_playlist('Default')
