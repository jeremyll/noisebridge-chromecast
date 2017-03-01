from time import sleep
import pychromecast
import pychromecast.controllers.youtube as youtube

import random

from scrap import get_list


chromecasts = pychromecast.get_chromecasts()
cast = None

for chromecast in chromecasts:
    if chromecast.device.friendly_name.startswith('Hackitorium'):
        cast = chromecast
        break

if not cast:
    print("No cast.. bye.. =(")
    exit()

yt = youtube.YouTubeController()
cast.register_handler(yt)

while True:
    print(cast.media_controller.status.player_state)
    if cast.media_controller.status.player_state == 'UNKNOWN':
        # Mute it so it doesn't annoy anyone 
        cast.volume_down(1)
        youtube_links = get_list()
        random_link = random.choice(youtube_links)
        print('next up: %s' % random_link)
        # Assume youtube link looks like this here:
        # 'https://www.youtube.com/watch?v=26AWdWr4AtA'
        # and we need just: '26AWdWr4AtA'
        youtube_id = random_link.split('=')[1]
        print(youtube_id)
        
        # Play next one
        yt.play_video(youtube_id)

    print('sleeping for 30..')
    sleep(30)
