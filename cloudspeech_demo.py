#!/usr/bin/env python3

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import re

import sys
sys.path.append('/home/pi/AIY-voice-kit-python/src/gMusicVoiceKit')
from SongManipulation.play_song import play_song
from SongManipulation.play_song_by_artist import play_song_by_artist
from PlaylistManipulation.create_playlist import create_playlist
from PlaylistManipulation.add_song_to_playlist import add_song_to_playlist

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('play')
    recognizer.expect_phrase('create a playlist named' or 'create playlist named')
    recognizer.expect_phrase('add')
    recognizer.expect_phrase('stop')
    isPlayInText = re.compile(r'\bplay\b')
    isStopInText = re.compile(r'^stop')

    button = aiy.voicehat.get_button()
    aiy.audio.get_recorder().start()

    if len(sys.arg) > 1 and sys.argv[1] is not None:
        text = sys.argv[1]
        print("Detected command line argument: " + text)

    while True:
        if text is None:
            print('Press the button and speak')
            aiy.audio.say('Waiting for command', volume=60)
            button.wait_for_press()
            print('Listening...')
            text = recognizer.recognize()
            
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            if 'stop' in text:
                stop = text.strip()
                if isStopInText.search(stop) is not None:
                    print("Stopping cloud speech...")
                    exit('Cloud speech was stopped.')
            if 'playlist named' in text:
                head, sep, tail = text.partition('named')
                aiy.audio.say('Creating playlist named ' + tail, volume=60)
                print('Creating playlist named ' + tail + '.')
                create_playlist(tail.strip())
                break
            elif isPlayInText.search(text) is not None:
                if 'by' in text:
                    song = text.replace('play', '').replace('by', '').strip()
                    head, sep, tail = song.partition(' ')

                    aiy.audio.say('Playing ' + head + ' by ' + tail + '.', volume=60)
                    print('Playing ' + head + ' by ' + tail + '.')
                    play_song_by_artist(head, tail)
                    break

                text = text.replace('play', '').strip()
                aiy.audio.say('Playing ' + text, volume=60)
                print('Playing ' + text + '.')
                play_song(text)
                break
            elif 'add' in text:
                text = text.replace('add', '')
                head, sep, tail = text.partition('to')

                aiy.audio.say('Adding ' + head + ' to ' + tail + '.', volume=60)
                print('Adding ' + head + ' to ' + tail + '.')
                add_song_to_playlist(head.strip(), tail.strip())
                break


if __name__ == '__main__':
    main()
