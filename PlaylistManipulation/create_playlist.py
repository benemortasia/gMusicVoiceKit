#!/usr/bin/env python
from gmusicapi import Mobileclient

gpm = Mobileclient()
# Login with username, password, and MAC.
# MAC helps Google Play Services identify the device
gpm.login('jpage628@gmail.com', pw, Mobileclient.FROM_MAC_ADDRESS)


def create_playlist(playlist_name="Default Playlist Title"):

    if Mobileclient.is_authenticated(gpm):
        all_playlists = Mobileclient.get_all_playlists(gpm)
        for playlist in all_playlists:
            print playlist
            temp = set()
            temp.add(playlist['name'])

        print temp
        # gpm.create_playlist(playlist_name)
    else:
        print "The Mobileclient is not authenticated."

    Mobileclient.logout(gpm)


# this will change based on voice input
create_playlist("A playlist name")
