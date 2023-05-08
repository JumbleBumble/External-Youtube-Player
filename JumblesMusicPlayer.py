import tkinter as tk
from tkinter import ttk
import youtube_dl
import subprocess
import threading
import urllib.request
from PIL import Image, ImageTk
import io
from io import BytesIO
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


window = tk.Tk()
window.title('Jumbles Music Player')
window.configure(bg='black')
style = ttk.Style()
style.configure('Custom.TButton', background='black', foreground = 'white')
label = tk.Label(master = window,bg="black", fg="white")
label.pack()


url = "https://blogger.googleusercontent.com/img/a/AVvXsEio-IZp3Tbblg1zP-SmExSXXWnA5U8aHT6t1c_s4K7yOyLSRryqFpCqRz4ucS85OeEsuZL2St9Re59We1iVR0H6ZKenZCv87vNj01Ni1F06ggcKGSe9rrOv3opvUpGfylbKQ8UhnNJ5iZGTlR40GFhBbXcFD0yHuKIPYWEs_xBpbflYaeVSS5jRAgsE=s500"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()
    
im = Image.open(io.BytesIO(raw_data))
im = im.resize((100, 100))
storedphoto = ImageTk.PhotoImage(im)
imagelabel = tk.Label(window, image = storedphoto,bg='black')
imagelabel.pack()






playing = False
process = None
def buttonfunc():
    global process
    global imagelabel
    global photo

    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    videoname = entry.get()
    label['text'] = 'Downloading Stream..'




    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f'ytsearch:{videoname}', download=False)
            label['text'] = 'Playing: ', info['entries'][0]['title']
        except youtube_dl.DownloadError:
            print('error youtube_dl.DownloadError')
            return
        except Exception as e:
            print(e)
            return

    yurl = f'https://www.youtube.com/watch?v={info["entries"][0]["id"]}'
    url = info['entries'][0]['formats'][0]['url']
    ThumbURL = f'https://img.youtube.com/vi/{info["entries"][0]["id"]}/0.jpg'
    with urllib.request.urlopen(ThumbURL) as u:
        raw_data = u.read()
    
        im = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)
        imagelabel.config(image = photo)
        imagelabel.config(width=200, height=200)
    cmd = f'ffmpeg -i "{url}" -vn -acodec libopus -b:a 96k -f opus -nostdin - | ffplay -nodisp -autoexit -'
    process = subprocess.Popen(cmd, shell=True)




def buttonfunc2(videoname):
    global process
    global label
    global playing
    global imagelabel
    global photo
    

    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    print(videoname)
    label['text'] = 'Downloading Stream..'




    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist = ydl.extract_info(videoname, download=False)
        except youtube_dl.DownloadError:
            print("Couldn't find any Playlist. (DOWNLOAD ERROR)")
            return
        except Exception as e:
            print(e)
            print("An error occurred while trying to find the Playlist.")
            return
        playing = True
        for song in playlist['entries']:
            if playing == False:
                return
            try:
                url = song['formats'][0]['url']
            except Exception as e:
                print(e)
                print("An error occurred while trying to play the video, Skipping to next in Playlist (URL ERROR)")
            yurl = f'https://www.youtube.com/watch?v={song["id"]}'
            ThumbURL = f'https://img.youtube.com/vi/{song["id"]}/0.jpg'
            with urllib.request.urlopen(ThumbURL) as u:
                raw_data = u.read()
            
                im = Image.open(io.BytesIO(raw_data))
                photo = ImageTk.PhotoImage(im)
                imagelabel.config(image = photo)
                imagelabel.config(width=200, height=200)
            cmd = f'ffmpeg -i "{url}" -vn -acodec libopus -b:a 96k -f opus -nostdin - | ffplay -nodisp -autoexit -'
            process = subprocess.Popen(cmd, shell=True)
            label['text'] = 'Playing: ', song['title']
            process.wait()
 

def threadstart():
    global t
    videoname = entry.get()
    t = threading.Thread(target=buttonfunc2,args=(videoname,))
    t.start()
  
def entrycheck(event):
    global process
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    videoname = entry.get()
    if 'list' in videoname:
        t = threading.Thread(target=buttonfunc2,args=(videoname,))
        t.start()
    else:
        buttonfunc()
def stopfunc():
    global process
    global playing
    global label
    global imagelabel
    global storedphoto
    label['text'] = ''
    imagelabel.config(image = storedphoto)
    imagelabel.config(width=100, height=100)
    playing = False
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")


def skipfunc():
    global process
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
       

entry = ttk.Entry(master = window)
entry.pack()

entry.bind('<Return>', entrycheck)


button = tk.Button(window, text = 'Play song by name search', bg="black", fg="white", command = buttonfunc)
button.pack()

button22 = tk.Button(master = window, text = 'Play Playlist', bg="black", fg="white", command = threadstart)
button22.pack()

Stopbutton = tk.Button(master = window, text = 'Stop', bg="black", fg="white", command = stopfunc)
Stopbutton.pack()

Skipbutton = tk.Button(master = window, text = 'Skip', bg="black", fg="white", command = skipfunc)
Skipbutton.pack()



def set_volume(volume):
    volume_level = float(volume) / 100.0
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "ffplay.exe":
            volume.SetMasterVolume(volume_level, None)
volume_slider = tk.Scale(window, from_=0, to=100,bg="black", fg="white", orient=tk.HORIZONTAL, command=set_volume)
volume_slider.pack()

window.mainloop()
