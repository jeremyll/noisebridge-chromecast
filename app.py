from time import sleep
import pychromecast
import pychromecast.controllers.youtube as youtube

import random

from scrap import get_list


#import logging
#logging.basicConfig(level=logging.DEBUG)


chromecasts = pychromecast.get_chromecasts()
cast = None

for chromecast in chromecasts:
    if chromecast.device.friendly_name.startswith('Hackitorium'):
        cast = chromecast
        break

if not cast:
    print("No cast.. bye.. =(")
    exit()

app_id = cast.app_id

last_videos = []
look_back = 10

while True:
    player_state = cast.media_controller.status.player_state
    current_app_id = cast.media_controller.app_id
    if player_state == 'UNKNOWN' or (
            player_state == 'IDLE'):
        # Mute it so it doesn't annoy anyone 
        cast.set_volume(0)

        youtube_links = get_list()
        look_back = min(len(youtube_links), look_back)
        random_link = random.choice(youtube_links)
        
        # Make sure the random_link hasn't been played recently
        while random_link in last_videos:
            random_link = random.choice(youtube_links)

        # Add choice to beginning of last_videos
        last_videos = [random_link] + last_videos
        # Pop the oldest off the list
        last_videos = last_videos[:look_back]

        print('next up: %s' % random_link)
        # Assume youtube link looks like this here:
        # 'https://www.youtube.com/watch?v=26AWdWr4AtA'
        # and we need just: '26AWdWr4AtA'
        youtube_id = random_link.split('=')[1]
        print(youtube_id)
        
        # Play next one
        yt = youtube.YouTubeController()
        cast.register_handler(yt)
        yt.play_video(youtube_id)

    sleep(3)
