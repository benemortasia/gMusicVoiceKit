#!/usr/bin/env python

# This program assumes the user has a subscription to Google Play Music.
# This program does not add songs from user purchased/uploaded songs, rather
# it takes the top hit(s) of a given song name.
from gmusicapi import Mobileclient
import re

gpm = Mobileclient()
# Login with username, password, and MAC.
# MAC helps Google Play Services identify the device
gpm.login('jpage628@gmail.com', pw, Mobileclient.FROM_MAC_ADDRESS)


def add_song_to_playlist(song="Raindrop Prelude", playlist_name="Default"):

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
        for i in playlists:
            print i['name']

            if re.match(playlist_pattern, i['name']):
                print "Playlist found!"
                search = gpm.search(song, 1)
                for track in search['song_hits']:
                    temp = dict(track['track'])
                    print temp
                    gpm.add_songs_to_playlist(i['id'], temp['storeId'])
                    print "Song " + temp['title'] + " was found, and placed in playlist: " + playlist_name
                break

    Mobileclient.logout(gpm)


add_song_to_playlist("Toccata and Fugue")
