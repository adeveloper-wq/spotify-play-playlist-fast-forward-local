import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
import os
import requests
from pygame import mixer
import time
from tkinter import *
from PIL import ImageTk
import PIL.Image
import requests
from tkinter import *  
from io import BytesIO
from urllib.request import urlopen
import _thread
import base64

from config import CLIENT_ID, CLIENT_SECRET

#IMPORTANT libmpg123-0.dll copied to C:\Windows\System32 and C:\Windows\SysWOW64
mixer.init()

def download(url: str, dest_folder: str, song_id: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    #filename = url.split('/')[-1].replace(" ", "_").replace("?", "_").replace("=", "_") + ".mp3"  # be careful with file names
    filename = song_id + ".mp3"
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

print(CLIENT_ID)
print(CLIENT_SECRET)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

# spotify:playlist:37i9dQZEVXbMDoHDwVN2tF --> Spotify Top 50 Global
# spotify:playlist:37i9dQZF1DWXDvpUgU6QYl
playlist_uri = input("Playlist URI: ")
print(playlist_uri.split(':'))
playlist_id = playlist_uri.split(':')[2]

playlist = sp.playlist(playlist_id)
playlist_name = playlist['name']
print(playlist_name)
Path(playlist_name).mkdir(parents=True, exist_ok=True)

tracks = sp.playlist_items(playlist_id, limit=100)

for track in tracks['items']:
    preview_url = track['track']['preview_url']
    song_id = track['track']['id']
    if (preview_url):
        #print(preview_url)
        download(preview_url, playlist_name, song_id)
        
main = Tk()
c = Canvas(main, width=640, height=640)
c.pack()

picture = PhotoImage(file='300.png')
picture2 = c.create_image(320,320,image=picture)
       
directory = os.fsencode(playlist_name)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mp3"): 
        mixer.music.load(playlist_name + '/' + filename)
        mixer.music.play( fade_ms= 500)
        song_id = filename.split(".")[0]
        track = sp.track(song_id)
        print(track)
        image_url = track['album']['images'][0]['url']
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()
        image = PIL.Image.open(BytesIO(raw_data))
        #img = ImageTk.PhotoImage(raw_data)
        
        global picture3
        picture3 = ImageTk.PhotoImage(image)
        c.itemconfigure(picture2, image = picture3)
        main.update()
        time.sleep(10)
        continue
    else:
        continue