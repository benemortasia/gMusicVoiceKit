#!/usr/bin/env python3

# This program assumes the user has a subscription to Google Play Music.
# This program does not add songs from user purchased/uploaded songs, rather
# it takes the top hit(s) of a given song name.
from gmusicapi import Mobileclient
from PlaylistManipulation.create_playlist import create_playlist
import re

__author__ = 'Jordan Page'
__license__ = 'MIT'
__version__ = '1.0.1'

gpm = Mobileclient()

# MAC helps Google Play Services identify the device
# *** Change EXAMPLE and PASSWORD to your own Gmail login. ***
gpm.login('EXAMPLE@gmail.com', 'PASSWORD',
          Mobileclient.FROM_MAC_ADDRESS)


def add_song_to_playlist(song, playlist_name):

    if Mobileclient.is_authenticated(gpm):

        # get_all_playlists() returns a dict object filled with
        # information about all of a user's playlists, and
        # each individual playlist is a dict as well.
        playlists = Mobileclient.get_all_playlists(gpm)
        # print playlists

        # one can get all playlist names by just accessing the
        # 'name' key of each playlist dict, as well as
        # compare the playlist name to a user given name
        playlist_pattern = re.compile(r'(?:.)*\s?(' + re.escape(playlist_name) + r')\s?(?:.)*', re.IGNORECASE)
        found = False

        for i in playlists:
            # print(i['name'])

            if re.match(playlist_pattern, i['name']):
                found = True
                print("Playlist found!")
                search = gpm.search(song, 1)
                
                for track in search['song_hits']:
                    temp = dict(track['track'])
                    # print(temp)
                    gpm.add_songs_to_playlist(i['id'], temp['storeId'])
                    print("Song " + temp['title'] + " was found, and placed in playlist: " + playlist_name)
                break

        if not found:
            i = create_playlist(playlist_name)
            print(playlist_name + ' was not found, but it was created.')

            search = gpm.search(song, 1)

            for track in search['song_hits']:
                temp = dict(track['track'])
                gpm.add_songs_to_playlist(i, temp['storeId'])
                print("Song " + temp['title'] + " was found, and placed in playlist: " + playlist_name)


    Mobileclient.logout(gpm)

# Useful if you want to test this function independently of cloudspeech
# Replace 'Raindrop Prelude' with some other song you may have
# and 'Default' with a playlist name
if __name__ == '__main__':
    add_song_to_playlist('Raindrop Prelude', 'Default')
