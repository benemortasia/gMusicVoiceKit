# gMusicVoiceKit

gMusicVoiceKit introduces four voice functions to the Voice AIY Kit (https://aiyprojects.withgoogle.com/voice-v1/) which play songs, create playlists, and add songs to playlists through Google Play Music through an already existing API, gmusicapi (https://unofficial-google-music-api.readthedocs.io/en/latest/).

Steps:
1. Follow the directions to build the Voice AIY Kit, if not built already (https://aiyprojects.withgoogle.com/voice-v1/). The gMusicVoiceKit functions are meant for version 1 of the Kit, and may or may not work for the newest version. The credentials part of the set-up is the most annoying part by far.
2. Once the Kit is up and running, open up the terminal and enter 'sudo apt-get update' followed by 'sudo apt-get upgrade'.
3. Before I could get gmusicapi to work correctly, something had to be installed regarding lxml. I believe the solution was to use 'sudo pip install lxml' in the terminal. After that, the typical installation for gmusicapi can be followed ('sudo pip install gmusicapi').
4. In the terminal, navigate to /src ('cd /home/pi/AIY-voice-kit-python/src') and then type 'git clone https://github.com/benemortasia/gMusicVoiceKit'
5. Take "cloudspeech_demo.py" and replace the one in /home/pi/AIY-voice-kit-python/src/examples/voice ('mv -f /home/pi/AIY-voice-kit-python/src/gMusicVoiceKit/cloudspeech_demo.py /home/pi/AIY-voice-kit-python/src/examples/voice'). This is the main script that interfaces the voice commands with each of the four functions.
6. If you want to activate the cloudspeech script when the Raspberry Pi starts up, take the "my_cloudspeech.service" file and put it in /lib/systemd/system. It can be deleted otherwise.
6b. Type ‘sudo raspi-config’ in terminal to change the Pi’s settings. Select Boot Settings and Enable Wait for Network at Boot.
6c. Lastly, type ‘sudo systemctl enable my_cloudspeech.service’ in terminal to enable the service at startup.
7. *** Make sure to change 'EXAMPLE@gmail.com' and 'PASSWORD' in each of the four functions or Google Play Music won't be able to be logged into. This can be done with nano or one of the few Python IDE's included with the Kit.
8. OAuth will have to be authorized two separate times: once for logging in with gmusicapi for the first time, and once for the button-press-to-stop-the-song mechanic. Just open up the URL and log in with your gmail to authorize it.
9. That should be it. Execute the cloudspeech_demo.py script at will, let it run at startup, or execute any of the four functions individually. Everyone is welcome to edit any of the included functions to explore more ideas or improve on this one.
