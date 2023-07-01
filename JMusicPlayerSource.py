import customtkinter as ctk
import youtube_dl
from youtube_search import YoutubeSearch
import subprocess
import threading
import urllib.request
from PIL import Image, ImageTk
import io
from io import BytesIO
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import os
import json
import re
import math
import time
import keyboard
import sys
import discordsdk as dsdk
import random
import math

app = dsdk.Discord(1108544841647927297, dsdk.CreateFlags.default)

activity_manager = app.get_activity_manager()

activity = dsdk.Activity()


def callback(result):
    if result == dsdk.Result.ok:
        print("Discord RPC: Successfully set the activity!")
    else:
        raise Exception(result)


if getattr(sys, 'frozen', False): 
    script_dir = os.path.abspath(sys._MEIPASS)
else:
    script_dir = os.path.abspath(os.path.dirname(__file__))

ffmpeg_path = os.path.join(script_dir, 'ffmpeg', 'bin', 'ffmpeg.exe')

if not any(os.access(os.path.join(path, 'ffmpeg.exe'), os.X_OK) for path in os.environ['PATH'].split(os.pathsep)):
    os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.join(script_dir, 'ffmpeg', 'bin'))
    os.environ['PATH'] = os.path.abspath(os.path.join(script_dir, 'ffmpeg', 'bin')) + os.pathsep + os.environ['PATH']

runfile_path = os.path.join(script_dir,'runfile.txt')




root = ctk.CTk()
root.geometry("300x420")
root.title("JMusicPlayer")
root.attributes("-topmost", False)
root.configure(fg_color='#1E2024')
root.rowconfigure(0,weight=10)
root.columnconfigure(0,weight=10)
#//ANCHOR - LOAD ICON
local_appdata_path = os.getenv('LOCALAPPDATA')
folder_path = os.path.join(local_appdata_path, 'JMusicPlayer')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
image_path = os.path.join(folder_path, 'JLuawlFav.ico')
if not os.path.exists(image_path):
    with urllib.request.urlopen('https://jumblescripts.com/JLuawlFav.ico') as u:
                    raw_data = u.read()
                    im = Image.open(io.BytesIO(raw_data))
                    im.save(image_path)             
if os.path.exists(image_path):
    root.iconbitmap(image_path)


file_path = os.path.join(folder_path, 'CurrentVol.json')
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        vol_dict = json.load(f)
        volume = vol_dict.get('CurrentVol')
else:
    volume = 100

progress_path = os.path.join(folder_path, 'progress.txt')
error_path = os.path.join(folder_path, 'videoerror.txt')

equalizer_path = os.path.join(folder_path, 'Equalizer.json')
if os.path.exists(equalizer_path):
    with open(equalizer_path, 'r') as f:
        equalizer_dict = json.load(f)
        if 'Equalizer' in equalizer_dict:
            EqualizerCheck = equalizer_dict['Equalizer']
        else:
            EqualizerCheck = False
        if 'Bass' in equalizer_dict:
            Bass = equalizer_dict['Bass']
        else:
            Bass = 0
        if 'Treble' in equalizer_dict:
            Treble = equalizer_dict['Treble']
        else:
            Treble = 0
else:
    equalizer_dict = {'Equalizer': False, 'Bass': 0, 'Treble': 0}
    EqualizerCheck = False
    Bass = 0
    Treble = 0




#//ANCHOR - UTILITY CLASSES
def CloseWindow(self):
    self.withdraw()

class NotificationWindow(ctk.CTkToplevel):
    def __init__(self,text,nclass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global Scriptentry
        #self.geometry("300x50")
        self.anchor = ctk.SE
        if nclass == 'Warning':
            self.title('Warning')
            self.label = ctk.CTkLabel(self,text_color='red', text=text)
        else:
            self.title('Success')
            self.label = ctk.CTkLabel(self,text_color='green', text=text)
        self.label.pack()
        self.okbutton = ctk.CTkButton(self,text='Ok',fg_color="black",hover_color='grey',command = lambda: CloseWindow(self))
        self.okbutton.pack()
        NewLen = len(text) * 5
        NewWidth=100 + NewLen
        self.geometry(f"{NewWidth}x50")
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()



#//ANCHOR - GUI & FUNCTIONS

MainFrame = ctk.CTkFrame(root,fg_color='#393E46',bg_color='#1E2024')
MainFrame.grid(column = 0, row = 0,sticky="nsew")
MainFrame.columnconfigure(0,weight=1000)
MainFrame.rowconfigure(0,weight=1000)
MainFrame.columnconfigure(1, weight=1000)
MainFrame.columnconfigure(2, weight=10)
MainFrame.columnconfigure(3, weight=10)
MainFrame.columnconfigure(4, weight=10)
MainFrame.columnconfigure(5, weight=10)
MainFrame.columnconfigure(6, weight=10)
MainFrame.rowconfigure(1, weight=1000)
MainFrame.rowconfigure(2, weight=1)
MainFrame.rowconfigure(3, weight=1)
MainFrame.rowconfigure(4, weight=1)
MainFrame.rowconfigure(5, weight=1)
MainFrame.rowconfigure(6, weight=1)

#//ANCHOR - LOAD DEFAULT THUMBNAIL
Label = ctk.CTkLabel(MainFrame,fg_color='#393E46',text_color='white',text='JMusicPlayer')
Label.grid(column = 0, row = 0,columnspan=2,sticky="nsew")
ThumbnailFrame = ctk.CTkFrame(MainFrame,fg_color='#393E46',bg_color='#1E2024')
ThumbnailFrame.grid(column = 0, row = 1,columnspan=2,sticky="nsew")
ThumbnailFrame.columnconfigure(0,weight=1000)
ThumbnailFrame.rowconfigure(0,weight=1000)
ThumbnailFrame.rowconfigure(1,weight=1000)
url = "https://blogger.googleusercontent.com/img/a/AVvXsEio-IZp3Tbblg1zP-SmExSXXWnA5U8aHT6t1c_s4K7yOyLSRryqFpCqRz4ucS85OeEsuZL2St9Re59We1iVR0H6ZKenZCv87vNj01Ni1F06ggcKGSe9rrOv3opvUpGfylbKQ8UhnNJ5iZGTlR40GFhBbXcFD0yHuKIPYWEs_xBpbflYaeVSS5jRAgsE=s500"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()
    
storedphoto = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(200, 200))
imagelabel = ctk.CTkLabel(ThumbnailFrame,text='', image = storedphoto,bg_color='#393E46')
imagelabel.grid(column=0,row=0,sticky="nsew")
imagelabel.columnconfigure(0,weight=1000)
imagelabel.rowconfigure(0,weight=1000)
imagelabel.rowconfigure(1,weight=1000)

VideoEntry = ctk.CTkEntry(MainFrame,width=250,placeholder_text="Search/URL")
VideoEntry.grid(column = 0, row = 2,columnspan=2,sticky="nsew")


ReplayCount = 0
LastReplay = None
SavedTime = None
MaxReplays =  20

def add_times(time1, time2):
    time1_parts = time1.split(':')
    time2_parts = time2.split(':')

    hours1 = int(time1_parts[0])
    minutes1 = int(time1_parts[1])
    seconds1 = float(time1_parts[2])

    hours2 = int(time2_parts[0])
    minutes2 = int(time2_parts[1])
    seconds2 = float(time2_parts[2])

    total_seconds = (hours1 + hours2) * 3600 + (minutes1 + minutes2) * 60 + seconds1 + seconds2

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    result = f'{hours:02}:{minutes:02}:{seconds:06.3f}'
    return result




def ResumePlayback(time_positiono):
    global process, CurrentVideo, CurrentURL, playing, volume, progress_path, EqualizerCheck, Bass, Treble, Paused, activity, error_path, ReplayCount, LastReplay, SavedTime, MaxReplays, Nightcore, Compand, Setrate, Ratevalue, Reverb, RevDelay, RevGain, Lofi, Slow, Chiptune, Bitcrush, Bitvalue, Swirl, SwirlDelay, SwirlDepth
    if LastReplay == CurrentURL:
        ReplayCount += 1
    else:
        ReplayCount = 0
    LastReplay = CurrentURL
    if ReplayCount >= MaxReplays:
        ReplayCount = 0
        return
    cmd = f'ffmpeg -i "{CurrentURL}" -vn -ss {time_positiono}'

    if EqualizerCheck or Nightcore or Chiptune or Slow or Lofi or Reverb or Compand or Setrate or Bitcrush or Swirl:
        cmd += ' -af "'
        if EqualizerCheck:
            cmd += f'equalizer=f=60:width_type=h:width=50:g={Bass},equalizer=f=8000:width_type=h:width=50:g={Treble},'
        if Nightcore:
            cmd += 'rubberband=tempo=1.25,'
        if Chiptune:
            cmd += 'aresample=8000,asetrate=8000,'
        if Slow:
            cmd += 'rubberband=pitch=0.7,asetrate=44100*0.7,'
        if Lofi:
            cmd += 'equalizer=f=125:width_type=h:width=200:g=-10,equalizer=f=250:width_type=h:width=200:g=-10,equalizer=f=500:width_type=h:width=200:g=-10,equalizer=f=1000:width_type=h:width=200:g=-10,equalizer=f=2000:width_type=h:width=200:g=-10,equalizer=f=4000:width_type=h:width=200:g=-10,equalizer=f=8000:width_type=h:width=200:g=-10,'
        if Reverb:
            cmd += f'aecho={RevGain}:0.9:1000:{RevDelay},'
        if Compand:
            cmd += 'compand=0.3|0.8:1|1:-90/-900|-70/-70|-20/-9|0/-3,'
        if Setrate:
            cmd += f'asetrate=44100{Ratevalue},'
        if Bitcrush:
            cmd += f'acrusher=bits={Bitvalue},'
        if Swirl:
            cmd += f'flanger=delay={SwirlDelay}:depth={SwirlDepth},'
        cmd += '"'
    
    cmd += f' -acodec libopus -b:a 96k -f opus -nostdin - -progress {progress_path} 2> {error_path} | ffplay -nodisp -autoexit -'
    process = subprocess.Popen(cmd, shell=True)
    set_volume(volume)
    process.wait()
    with open(error_path, 'r') as file:
        error_output = file.read()
    time.sleep(0.1)
    with open(error_path, 'w'):
        pass
    if 'Error demuxing' in error_output:
        matches = re.findall(r'time=([0-9:.]+)', error_output)
        if len(matches) > 0:
            time_position = matches[-1]
            if SavedTime != None:
                time_positiony = add_times(SavedTime,time_position)
                SavedTime = add_times(SavedTime,time_position)
                ResumePlayback(time_positiony)
            else:
                ResumePlayback(time_position)









#//ANCHOR - PLAYSEARCH
Amount = 0
CurrentVideo = None
CurrentURL = None
playing = False
process = None
Paused = False
MaxDuration = None
Nightcore = False
Compand = False
Setrate = False
Ratevalue = '*1.5'
Reverb = False
RevDelay = '0.3'
RevGain = '0.8'
Lofi = False
Slow = False
Chiptune = False
Bitcrush = False
Bitvalue = '4'
Swirl = False
SwirlDelay = '0.003'
SwirlDepth = '7'
def PlaySearch(videoname):
    global process, imagelabel, photo, Amount, CurrentVideo, CurrentURL, playing, volume, progress_path, EqualizerCheck, Bass, Treble, Paused, activity, error_path, SavedTime, Nightcore, Compand, MaxDuration, Setrate, Ratevalue, Reverb, RevDelay, RevGain, Lofi, Slow, Chiptune, Bitcrush, Bitvalue, Swirl, SwirlDelay, SwirlDepth, runfile_path

    MaxDuration = None
    Nightcore = False
    Compand = False
    Setrate = False
    Ratevalue = '*1.5'
    Reverb = False
    RevDelay = '0.3'
    RevGain = '0.8'
    Lofi = False
    Slow = False
    Chiptune = False
    Bitcrush = False
    Bitvalue = '4'
    Swirl = False
    SwirlDelay = '0.003'
    SwirlDepth = '7'


    Label.configure(text='Downloading Stream..')

    def shuffle_list(lst):
        result = lst.copy()
        random.shuffle(result)
        return result

    def Handle_Type(videoname):
        global Compand, MaxDuration, Setrate, Ratevalue, Reverb, RevDelay, RevGain, Lofi, Slow, Chiptune, Bitcrush, Bitvalue, Swirl, SwirlDelay, SwirlDepth, runfile_path
        if 'jrunfile' in videoname.lower():
            if '+' in videoname:
                runsplit = videoname.split('+')
                runfile_path = os.path.join(script_dir,f'runfile{runsplit[1]}.txt')
            if os.path.exists(runfile_path):
                videoname = open(runfile_path,'r').read()
            else:
                NotificationWindow(text=f'runfile Not Found. Make sure its located in the same folder as the players exe/source and named runfile.txt',nclass='Warning')
        if ':' in videoname:
            Multi = videoname.split(':')
            resultlist = []
            for index,name in enumerate(Multi):
                lenminus = 0
                if index != 0:
                    videoname = videoname.replace(':'+name,'')
                if 'duration' in name:
                    DurSplit = name.split('=')
                    lenminus += 1
                    MaxDuration = int(DurSplit[1])
                    if MaxDuration < 0:
                        MaxDuration = 0
                    continue
                if 'nightcore' in name:
                    lenminus += 1
                    Nightcore = True
                    continue
                if 'compand' in name:
                    lenminus += 1
                    Compand = True
                    continue
                if 'setrate' in name:
                    if '=' in name:
                        RateSplit = name.split('=')
                        Ratevalue = RateSplit[1]
                    else:
                        Ratevalue = '*1.5'
                    lenminus += 1
                    Setrate = True
                    continue
                if 'reverb' in name:
                    lenminus += 1
                    if '=' in name:
                        RevSplit = name.split('=')
                        if ',' in RevSplit[1]:
                            RBSplit = RevSplit[1].split(',')
                            RevGain = RBSplit[0]
                            if float(RevGain) > 1:
                                RevGain = '1.0'
                            if float(RevGain) < 0:
                                RevGain = '0'
                            RevDelay = RBSplit[1]
                            if float(RevDelay) > 1:
                                RevDelay = '1'
                            if float(RevDelay) < 0.1:
                                RevDelay = '0.1'
                        else:
                            RevDelay = RevSplit[1]
                            if float(RevDelay) > 1:
                                RevDelay = '1'
                            if float(RevDelay) < 0.1:
                                RevDelay = '0.1'
                    Reverb = True
                    continue
                if 'lofi' in name:
                    lenminus += 1
                    Lofi = True
                    continue
                if 'slow' in name:
                    lenminus += 1
                    Slow = True
                    continue
                if 'chiptune' in name:
                    lenminus += 1
                    Chiptune = True
                    continue
                if 'bitcrush' in name:
                    if '=' in name:
                        bitSplit = name.split('=')
                        Bitvalue = bitSplit[1]
                    else:
                        Bitvalue = '4'
                    lenminus += 1
                    Bitcrush = True
                    continue
                if 'swirl' in name:
                    lenminus += 1
                    if '=' in name:
                        SwirlSplit = name.split('=')
                        if ',' in SwirlSplit[1]:
                            SWSplit = SwirlSplit[1].split(',')
                            SwirlDelay = SWSplit[0]
                            SwirlDepth = SWSplit[1]
                            if float(SwirlDepth) > 10:
                                SwirlDepth = '10'
                        else:
                            SwirlDepth = SwirlSplit[1]
                            if float(SwirlDepth) > 10:
                                SwirlDepth = '10'
                    Swirl = True
                    continue

                tempresult = YoutubeSearch(name, max_results=math.floor(int(Amount) / (len(Multi)-lenminus))).to_dict()
                resultlist += tempresult
                
            results = shuffle_list(resultlist)
         
            return results,videoname
        else:
            return False,videoname
        
    def get_CMD():
        cmd = f'ffmpeg -i "{url}" -vn'
        if EqualizerCheck or Nightcore or Chiptune or Slow or Lofi or Reverb or Compand or Setrate or Bitcrush or Swirl:
                cmd += ' -af "'
                if EqualizerCheck:
                    cmd += f'equalizer=f=60:width_type=h:width=50:g={Bass},equalizer=f=8000:width_type=h:width=50:g={Treble},'
                if Nightcore:
                    cmd += 'rubberband=tempo=1.25,'
                if Chiptune:
                    cmd += 'aresample=8000,asetrate=8000,'
                if Slow:
                    cmd += 'rubberband=pitch=0.7,asetrate=44100*0.7,'
                if Lofi:
                    cmd += 'equalizer=f=125:width_type=h:width=200:g=-10,equalizer=f=250:width_type=h:width=200:g=-10,equalizer=f=500:width_type=h:width=200:g=-10,equalizer=f=1000:width_type=h:width=200:g=-10,equalizer=f=2000:width_type=h:width=200:g=-10,equalizer=f=4000:width_type=h:width=200:g=-10,equalizer=f=8000:width_type=h:width=200:g=-10,'
                if Reverb:
                    cmd += f'aecho={RevGain}:0.9:1000:{RevDelay},'
                if Compand:
                    cmd += 'compand=0.3|0.8:1|1:-90/-900|-70/-70|-20/-9|0/-3,'
                if Setrate:
                    cmd += f'asetrate=44100{Ratevalue},'
                if Bitcrush:
                    cmd += f'acrusher=bits={Bitvalue},'
                if Swirl:
                    cmd += f'flanger=delay={SwirlDelay}:depth={SwirlDepth},'
                cmd += '"'
        cmd += f' -acodec libopus -b:a 96k -f opus -nostdin - -progress {progress_path} 2> {error_path} | ffplay -nodisp -autoexit -'
        return cmd

    if Amount == 0:
        results,videoname=Handle_Type(videoname)
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
                title = info['entries'][0]['title']
                Label.configure(text=f'Playing: {title}')
            except youtube_dl.DownloadError:
                NotificationWindow(text=f'youtube_dl.DownloadError',nclass='Warning')
                return
            except Exception as e:
                NotificationWindow(text=f'Error: {e}',nclass='Warning')
                return
            url = info['entries'][0]['url']
            CurrentVideo = info['entries'][0]['title']
            activity.state = f"Playing: {CurrentVideo}"
            activity_manager.update_activity(activity, callback)
            CurrentURL = info['entries'][0]['url']
            ThumbID = info['entries'][0]['id']
            ThumbURL = f'https://img.youtube.com/vi/{ThumbID}/0.jpg'
            with urllib.request.urlopen(ThumbURL) as u:
                raw_data = u.read()
                photo = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(250, 200))
                imagelabel.configure(image = photo)
            cmd = get_CMD()
            process = subprocess.Popen(cmd, shell=True)
            set_volume(volume)
            process.wait()
            with open(error_path, 'r') as file:
                error_output = file.read()
            time.sleep(0.1)
            with open(error_path, 'w'):
                pass
            if 'Error demuxing' in error_output:
                print('DEMUXING ERROR - REPLAYING')
                if os.path.exists(progress_path):
                    with open(progress_path, 'r') as f:
                        progress_data = f.read()
                    matches = re.findall(r'time=([0-9:.]+)', progress_data)
                    if len(matches) > 0:
                        time_position = matches[-1]
                        SavedTime = time_position
                        ResumePlayback(time_position)


    else:
        if Amount == 'All' or Amount == 'all':
            Amount = 1000
        results,videoname = Handle_Type(videoname)
        if results == False:  
            results = YoutubeSearch(videoname, max_results=int(Amount)).to_dict()
        playing = True
        for song in results:
            if playing == False:
                return
            while Paused:
                time.sleep(0.5)
            if playing == False:
                return
            songduration = song['duration']
            if MaxDuration != None:
                songdursplit = songduration.split(':')
                if int(songdursplit[0]) > MaxDuration or len(songdursplit) == 3:
                    continue
            rurl = f'https://www.youtube.com{song["url_suffix"]}'
            ThumbURL = song['thumbnails'][0]
            with urllib.request.urlopen(ThumbURL) as u:
                raw_data = u.read()
                photo = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(250, 200))
                imagelabel.configure(image = photo)
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
                    info = ydl.extract_info(rurl, download=False)
                    title = info['title']
                    Label.configure(text=f'Playing: {title}')
                except youtube_dl.DownloadError:
                    NotificationWindow(text=f'youtube_dl.DownloadError: {e}',nclass='Warning')
                    return
                except Exception as e:
                    NotificationWindow(text=f'Error: {e}',nclass='Warning')
                    return

            try:
                url = info['formats'][0]['url']
                CurrentVideo = info['title']
                activity.state = f"Playing: {CurrentVideo}"
                activity_manager.update_activity(activity, callback)
                CurrentURL = info['formats'][0]['url']
            except Exception as e:
                NotificationWindow(text=f'Error: {e} (Most likely ran out of videos)',nclass='Warning')
            ThumbURL = f'https://img.youtube.com/vi/{info["id"]}/0.jpg'
            with urllib.request.urlopen(ThumbURL) as u:
                raw_data = u.read()
                photo = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(250, 200))
                imagelabel.configure(image = photo)
            cmd = get_CMD()
            process = subprocess.Popen(cmd, shell=True)
            set_volume(volume)
            process.wait()
            with open(error_path, 'r') as file:
                error_output = file.read()
            time.sleep(0.1)
            with open(error_path, 'w'):
                pass
            if 'Error demuxing' in error_output:
                print('DEMUXING ERROR - REPLAYING')
                if os.path.exists(progress_path):
                    with open(progress_path, 'r') as f:
                        progress_data = f.read()
                    matches = re.findall(r'time=([0-9:.]+)', progress_data)
                    if len(matches) > 0:
                        time_position = matches[-1]
                        SavedTime = time_position
                        ResumePlayback(time_position)




    

def PlaySearchthreadstart():
    global process, playing, storedphoto, Paused, InterPaused
    InterPaused = False
    Paused = False
    playing = False
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    global t
    videoname = VideoEntry.get()
    t = threading.Thread(target=PlaySearch,args=(videoname,))
    t.start()

PlaySearchbutton = ctk.CTkButton(MainFrame, text="Play song by search",fg_color="black",hover_color='grey',bg_color='#393E46',command=PlaySearchthreadstart)
PlaySearchbutton.grid(column = 0, row = 3,padx=1,pady=1,sticky="nsew")



def SetAmount():
    global Amount
    dialog = ctk.CTkInputDialog(text="Set amount of songs you'd like to play using search:", title="Amount Set")
    Amount = dialog.get_input()



EditAmountbutton = ctk.CTkButton(MainFrame, text="Song Amount",fg_color="black",hover_color='grey',bg_color='#393E46',command=SetAmount)
EditAmountbutton.grid(column = 1, row = 3,padx=1,pady=1,sticky="nsew")








#//ANCHOR - PLAYLIST
def Playlistfunc(videoname):
    global process, playing, imagelabel, photo, CurrentVideo, CurrentURL, volume, progress_path, EqualizerCheck, Bass, Treble, Paused, Amount, activity, SavedTime, Nightcore, Compand, Setrate, Ratevalue, Reverb, RevDelay, RevGain, Lofi, Slow, Chiptune, Bitcrush, Bitvalue, Swirl, SwirlDelay, SwirlDepth

    Nightcore = False
    Compand = False
    Setrate = False
    Ratevalue = '*1.5'
    Reverb = False
    RevDelay = '0.3'
    RevGain = '0.8'
    Lofi = False
    Slow = False
    Chiptune = False
    Bitcrush = False
    Bitvalue = '4'
    Swirl = False
    SwirlDelay = '0.003'
    SwirlDepth = '7'


    

    Label.configure(text='Downloading Stream..')
    if Amount == 'All' or Amount == 'all' or Amount == 0:
        Amount = 99999999


    if ':' in videoname:
            Multi = videoname.split(':')
            for index,name in enumerate(Multi):
                if index != 0 and index != 1:
                    videoname = videoname.replace(':'+name,'')
                if 'nightcore' in name:
                    Nightcore = True
                    continue
                if 'compand' in name:
                    Compand = True
                    continue
                if 'setrate' in name:
                    if '=' in name:
                        RateSplit = name.split('=')
                        RateValue = RateSplit[1]
                    else:
                        RateValue = '*1.5'
                    Setrate = True
                    continue
                if 'reverb' in name:
                    if '=' in name:
                        RevSplit = name.split('=')
                        if ',' in RevSplit[1]:
                            RBSplit = RevSplit[1].split(',')
                            RevGain = RBSplit[0]
                            if float(RevGain) > 1:
                                RevGain = '1.0'
                            if float(RevGain) < 0:
                                RevGain = '0'
                            RevDelay = RBSplit[1]
                            if float(RevDelay) > 1:
                                RevDelay = '1'
                            if float(RevDelay) < 0.1:
                                RevDelay = '0.1'
                        else:
                            RevDelay = RevSplit[1]
                            if float(RevDelay) > 1:
                                RevDelay = '1'
                            if float(RevDelay) < 0.1:
                                RevDelay = '0.1'
                    Reverb = True
                    continue
                if 'lofi' in name:
                    Lofi = True
                    continue
                if 'slow' in name:
                    Slow = True
                    continue
                if 'chiptune' in name:
                    Chiptune = True
                    continue
                if 'bitcrush' in name:
                    if '=' in name:
                        bitSplit = name.split('=')
                        Bitvalue = bitSplit[1]
                    else:
                        Bitvalue = '4'
                    Bitcrush = True
                    continue
                if 'swirl' in name:
                    if '=' in name:
                        SwirlSplit = name.split('=')
                        if ',' in SwirlSplit[1]:
                            SWSplit = SwirlSplit[1].split(',')
                            SwirlDelay = SWSplit[1]
                            SwirlDepth = SWSplit[0]
                            if float(SwirlDepth) > 10:
                                SwirlDepth = '10'
                        else:
                            SwirlDepth = SwirlSplit[0]
                            if float(SwirlDepth) > 10:
                                SwirlDepth = '10'
                    Swirl = True
                    continue
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'playlistend': int(Amount),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist = ydl.extract_info(videoname, download=False)
        except youtube_dl.DownloadError:
            NotificationWindow(text=f'youtube_dl.DownloadError: {e}',nclass='Warning')
            return
        except Exception as e:
            NotificationWindow(text=f'Error: {e}',nclass='Warning')
            return
        playing = True
        for song in playlist['entries']:
            if playing == False:
                return
            while Paused:
                time.sleep(0.5)
            if playing == False:
                return
            try:
                url = song['formats'][0]['url']
                CurrentURL = song['formats'][0]['url']
            except Exception as e:
                NotificationWindow(text=f'An error occurred while trying to play the video, Skipping to next in Playlist (URL ERROR)',nclass='Warning')

            ThumbURL = f'https://img.youtube.com/vi/{song["id"]}/0.jpg'
            with urllib.request.urlopen(ThumbURL) as u:
                raw_data = u.read()
                photo = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(250, 200))
                imagelabel.configure(image = photo)
            CurrentVideo = song['title']
            activity.state = f"Playing: {CurrentVideo}"
            activity_manager.update_activity(activity, callback)
            cmd = f'ffmpeg -i "{url}" -vn'
    
            if EqualizerCheck or Nightcore or Chiptune or Slow or Lofi or Reverb or Compand or Setrate or Bitcrush or Swirl:
                cmd += ' -af "'
                if EqualizerCheck:
                    cmd += f'equalizer=f=60:width_type=h:width=50:g={Bass},equalizer=f=8000:width_type=h:width=50:g={Treble},'
                if Nightcore:
                    cmd += 'rubberband=tempo=1.25,'
                if Chiptune:
                    cmd += 'aresample=8000,asetrate=8000,'
                if Slow:
                    cmd += 'rubberband=pitch=0.7,asetrate=44100*0.7,'
                if Lofi:
                    cmd += 'equalizer=f=125:width_type=h:width=200:g=-10,equalizer=f=250:width_type=h:width=200:g=-10,equalizer=f=500:width_type=h:width=200:g=-10,equalizer=f=1000:width_type=h:width=200:g=-10,equalizer=f=2000:width_type=h:width=200:g=-10,equalizer=f=4000:width_type=h:width=200:g=-10,equalizer=f=8000:width_type=h:width=200:g=-10,'
                if Reverb:
                    cmd += f'aecho={RevGain}:0.9:1000:{RevDelay},'
                if Compand:
                    cmd += 'compand=0.3|0.8:1|1:-90/-900|-70/-70|-20/-9|0/-3,'
                if Setrate:
                    cmd += f'asetrate=44100{Ratevalue},'
                if Bitcrush:
                    cmd += f'acrusher=bits={Bitvalue},'
                if Swirl:
                    cmd += f'flanger=delay={SwirlDelay}:depth={SwirlDepth},'
                cmd += '"'
            
            cmd += f' -acodec libopus -b:a 96k -f opus -nostdin - -progress {progress_path} 2> {error_path} | ffplay -nodisp -autoexit -'

            process = subprocess.Popen(cmd, shell=True)
            set_volume(volume)
            labtitle = 'Playing: ', song['title']
            Label.configure(text=labtitle)
            process.wait()
            with open(error_path, 'r') as file:
                error_output = file.read()
            time.sleep(1)
            with open(error_path, 'w'):
                pass
            if 'Error demuxing' in error_output:
                print('DEMUXING ERROR - REPLAYING')
                if os.path.exists(progress_path):
                    with open(progress_path, 'r') as f:
                        progress_data = f.read()
                    matches = re.findall(r'time=([0-9:.]+)', progress_data)
                    if len(matches) > 0:
                        time_position = matches[-1]
                        SavedTime = time_position
                        ResumePlayback(time_position)





def Playlistthreadstart():
    global process, playing, storedphoto, Paused, InterPaused
    InterPaused = False
    Paused = False
    playing = False
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    global tt
    videoname = VideoEntry.get()
    tt = threading.Thread(target=Playlistfunc,args=(videoname,))
    tt.start()

Playlistbutton = ctk.CTkButton(MainFrame, text="Play Playlist",fg_color="black",hover_color='grey',bg_color='#393E46',command=Playlistthreadstart)
Playlistbutton.grid(column = 0, row = 4,padx=1,pady=1,sticky="nsew")










#//ANCHOR - DOWNLOAD
def downloadfunc(videoname):
    if 'list' in videoname:
        ydl_opts = {
            'outtmpl': os.path.join(os.path.dirname(os.path.abspath(__file__)), '%(title)s.%(ext)s'),
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
                NotificationWindow(text=f'youtube_dl.DownloadError: {e}',nclass='Warning')
                return
            except Exception as e:
                NotificationWindow(text=f'Error: {e}',nclass='Warning')
                return
            for song in playlist['entries']:
                try:
                    url = song['formats'][0]['url']
                except Exception as e:
                    print(e)
                yurl = f'https://www.youtube.com/watch?v={song["id"]}'
                ThumbURL = f'https://img.youtube.com/vi/{song["id"]}/0.jpg'
                with urllib.request.urlopen(ThumbURL) as u:
                    raw_data = u.read()
                photo = ctk.CTkImage(light_image=Image.open(io.BytesIO(raw_data)),
                                  dark_image=Image.open(io.BytesIO(raw_data)),
                                  size=(250, 200))
                imagelabel.configure(image = photo)
                labtitle = 'Downloading ', song['title'], '...'
                Label.configure(text=labtitle)
                ydl.download([yurl])
                label['text'] = 'Downloaded to ', {str(os.path.join(os.path.dirname(os.path.abspath(__file__))))}
        
        labtitle = 'Downloaded to ', {str(os.path.join(os.path.dirname(os.path.abspath(__file__))))}
        Label.configure(text=labtitle)
    else:
        ydl_opts = {
        'outtmpl': os.path.join(os.path.dirname(os.path.abspath(__file__)), '%(title)s.%(ext)s'),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
    }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{videoname}', download=False)
            url = f'https://www.youtube.com/watch?v={info["entries"][0]["id"]}'
            labtitle = 'Downloading ', info['entries'][0]['title'], '...'
            Label.configure(text=labtitle)
            ydl.download([url])
            labtitle = 'Downloaded to ', {str(os.path.join(os.path.dirname(os.path.abspath(__file__))))}
            Label.configure(text=labtitle)

def Downloadthreadstart():
    global CurrentVideo
    if CurrentVideo != None:
        videoname = CurrentVideo
    else:
        videoname = VideoEntry.get()
    thread = threading.Thread(target=downloadfunc,args=(videoname,))
    thread.start()

Downloadbutton = ctk.CTkButton(MainFrame, text="Download",fg_color="black",hover_color='grey',bg_color='#393E46',command=Downloadthreadstart)
Downloadbutton.grid(column = 1, row = 4,padx=1,pady=1,sticky="nsew")









#//ANCHOR - STOP
def stopfunc():
    global process, playing, label, imagelabel, storedphoto, Paused, InterPaused
    Label.configure(text='JMusicPlayer')
    imagelabel.configure(image = storedphoto)
    InterPaused = False
    Paused = False
    playing = False
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")

Stopbutton = ctk.CTkButton(MainFrame, text="Stop",fg_color="black",hover_color='grey',bg_color='#393E46',command=stopfunc)
Stopbutton.grid(column = 0, row = 5,padx=1,pady=1,sticky="nsew")


StopKeySet = False
StopKey = None
def StopSetFocus(event):
    Stopbutton.configure(text='Enter Keybind') 
    Stopbutton.focus()
    Stopbutton.bind('<KeyPress>', StopSetKey, add='+')

def StopSetKey(event):
    global StopKey
    global StopKeySet
    Stopbutton.configure(text='Stop') 
    Stopbutton.unbind('<KeyPress>')
    try:
        if event.keysym:
            StopKey = event.keysym
            StopKeySet = True
            NotificationWindow(text=f'Stop Keybind Set: Shift + {event.keysym}',nclass='W')
    except Exception as e:
        NotificationWindow(text=f'Keybind Error: {e}',nclass='Warning')



Stopbutton.bind('<Button>',StopSetFocus)






#//ANCHOR - SKIP
def skipfunc():
    global process
    global CurrentURL
    global Paused
    global InterPaused
    CurrentURL = ''
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    Paused = False
    InterPaused = False



Skipbutton = ctk.CTkButton(MainFrame, text="Skip",fg_color="black",hover_color='grey',bg_color='#393E46',command=skipfunc)
Skipbutton.grid(column = 1, row = 5,padx=1,pady=1,sticky="nsew")

SkipKeySet = False
SkipKey = None
def SkipSetFocus(event):
    Skipbutton.configure(text='Enter Keybind') 
    Skipbutton.focus()
    Skipbutton.bind('<KeyPress>', SkipSetKey, add='+')

def SkipSetKey(event):
    global SkipKey
    global SkipKeySet
    Skipbutton.configure(text='Skip') 
    Skipbutton.unbind('<KeyPress>')
    try:
        if event.keysym:
            SkipKey = event.keysym
            SkipKeySet = True
            NotificationWindow(text=f'Skip Keybind Set: Shift + {event.keysym}',nclass='W')
    except Exception as e:
        NotificationWindow(text=f'Keybind Error: {e}',nclass='Warning')



Skipbutton.bind('<Button>',SkipSetFocus)


InterPaused = False
#//ANCHOR - PAUSE
def Pausefunc():
    global process
    global Paused
    global InterPaused
    if Paused:
        InterPaused = True
    Paused = True
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")



Pausebutton = ctk.CTkButton(MainFrame, text="Pause",fg_color="black",hover_color='grey',bg_color='#393E46',command=Pausefunc)
Pausebutton.grid(column = 0, row = 6,padx=1,pady=1,sticky="nsew")

PauseKeySet = False
PauseKey = None
def PauseSetFocus(event):
    Pausebutton.configure(text='Enter Keybind') 
    Pausebutton.focus()
    Pausebutton.bind('<KeyPress>', PauseSetKey, add='+')

def PauseSetKey(event):
    global PauseKey
    global PauseKeySet
    Pausebutton.configure(text='Pause') 
    Pausebutton.unbind('<KeyPress>')
    try:
        if event.keysym:
            PauseKey = event.keysym
            PauseKeySet = True
            NotificationWindow(text=f'Pause Keybind Set: Shift + {event.keysym}',nclass='W')
    except Exception as e:
        NotificationWindow(text=f'Keybind Error: {e}',nclass='Warning')



Pausebutton.bind('<Button>',PauseSetFocus)

threado = None
#//ANCHOR - RESUME
def Resumefunc():
    global process, playing, imagelabel, photo, CurrentVideo, CurrentURL, volume, progress_path, EqualizerCheck, Bass, Treble, Paused, Amount, activity, SavedTime, Nightcore, Compand, Setrate, Ratevalue, Reverb, RevDelay, RevGain, Lofi, Slow, Chiptune, Bitcrush, Bitvalue, Swirl, SwirlDelay, SwirlDepth, threado, InterPaused
    OldURL = CurrentURL
    if os.path.exists(progress_path) and process == None:
        with open(progress_path, 'r') as f:
            progress_data = f.read()
        matches = re.findall(r'time=([0-9:.]+)', progress_data)
        if len(matches) > 0:
            time_position = matches[-1]
        cmd = f'ffmpeg -i "{url}" -vn -ss {time_position}'
    
        if EqualizerCheck or Nightcore or Chiptune or Slow or Lofi or Reverb or Compand or Setrate or Bitcrush or Swirl:
            cmd += ' -af "'
            if EqualizerCheck:
                cmd += f'equalizer=f=60:width_type=h:width=50:g={Bass},equalizer=f=8000:width_type=h:width=50:g={Treble},'
            if Nightcore:
                cmd += 'rubberband=tempo=1.25,'
            if Chiptune:
                cmd += 'aresample=8000,asetrate=8000,'
            if Slow:
                cmd += 'rubberband=pitch=0.7,asetrate=44100*0.7,'
            if Lofi:
                cmd += 'equalizer=f=125:width_type=h:width=200:g=-10,equalizer=f=250:width_type=h:width=200:g=-10,equalizer=f=500:width_type=h:width=200:g=-10,equalizer=f=1000:width_type=h:width=200:g=-10,equalizer=f=2000:width_type=h:width=200:g=-10,equalizer=f=4000:width_type=h:width=200:g=-10,equalizer=f=8000:width_type=h:width=200:g=-10,'
            if Reverb:
                cmd += f'aecho={RevGain}:0.9:1000:{RevDelay},'
            if Compand:
                cmd += 'compand=0.3|0.8:1|1:-90/-900|-70/-70|-20/-9|0/-3,'
            if Setrate:
                cmd += f'asetrate=44100{Ratevalue},'
            if Bitcrush:
                cmd += f'acrusher=bits={Bitvalue},'
            if Swirl:
                cmd += f'flanger=delay={SwirlDelay}:depth={SwirlDepth},'
            cmd += '"'
        
        cmd += f' -acodec libopus -b:a 96k -f opus -nostdin - -progress {progress_path} 2> {error_path} | ffplay -nodisp -autoexit -'
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        with open(error_path, 'r') as file:
            error_output = file.read()
        time.sleep(1)
        with open(error_path, 'w'):
            pass
        if 'Error demuxing' in error_output:
            print('DEMUXING ERROR - REPLAYING')
            if os.path.exists(progress_path):
                with open(progress_path, 'r') as f:
                    progress_data = f.read()
                matches = re.findall(r'time=([0-9:.]+)', progress_data)
                if len(matches) > 0:
                    time_position = matches[-1]
                    SavedTime = time_position
                    ResumePlayback(time_position)
        threado = None
        if not InterPaused:
            Paused = False
        InterPaused = False

def Resumefuncthreadstart():
    global threado
    if threado == None:
        threado = threading.Thread(target=Resumefunc)
        threado.start()
Resumebutton = ctk.CTkButton(MainFrame, text="Resume",fg_color="black",hover_color='grey',bg_color='#393E46',command=Resumefuncthreadstart)
Resumebutton.grid(column = 1, row = 6,padx=1,pady=1,sticky="nsew")

ResumeKeySet = False
ResumeKey = None
def ResumeSetFocus(event):
    Resumebutton.configure(text='Enter Keybind') 
    Resumebutton.focus()
    Resumebutton.bind('<KeyPress>', ResumeSetKey, add='+')

def ResumeSetKey(event):
    global ResumeKey
    global ResumeKeySet
    Resumebutton.configure(text='Resume') 
    Resumebutton.unbind('<KeyPress>')
    try:
        if event.keysym:
            ResumeKey = event.keysym
            ResumeKeySet = True
            NotificationWindow(text=f'Resume Keybind Set: Shift + {event.keysym}',nclass='W')
    except Exception as e:
        NotificationWindow(text=f'Keybind Error: {e}',nclass='Warning')



Resumebutton.bind('<Button>',ResumeSetFocus)

class EqualizerWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global EqualizerCheck
        global Bass
        global Treble
        self.geometry("560x180")
        self.title('Equalizers')
        self.columnconfigure(0,weight=1)
        BassLabel = ctk.CTkLabel(self,text_color='white',text='Bass')
        BassLabel.grid(column = 0, row = 0,columnspan=2,sticky="nsew")
        BassGLabel = ctk.CTkLabel(self,text_color='white',text=str(math.floor(Bass)))
        BassGLabel.grid(column = 0, row = 1,columnspan=2,sticky="nsew")
        def Set_Bass(volume):
            global Bass
            Bass = volume
            BassGLabel.configure(text=str(math.floor(volume)))
            equalizer_dict['Bass'] = volume
            if os.path.exists(folder_path):
                with open(equalizer_path, 'w') as f:
                        json.dump(equalizer_dict, f)
        BassG_var = ctk.IntVar(value=0)
        bass_slider = ctk.CTkSlider(self,variable=BassG_var, from_=-100, to=100,bg_color="black", fg_color="white", command=Set_Bass)
        bass_slider.grid(column = 0, row = 2,columnspan=2,sticky="nsew")
        bass_slider.set(Bass)
        def Set_Treble(volume):
            global Treble
            Treble = volume
            TrebleGLabel.configure(text=str(math.floor(volume)))
            equalizer_dict['Treble'] = volume
            if os.path.exists(folder_path):
                with open(equalizer_path, 'w') as f:
                        json.dump(equalizer_dict, f)
        TrebleLabel = ctk.CTkLabel(self,text_color='white',text='Treble')
        TrebleLabel.grid(column = 0, row = 3,pady=2,columnspan=2,sticky="nsew")
        TrebleGLabel = ctk.CTkLabel(self,text_color='white',text=str(math.floor(Treble)))
        TrebleGLabel.grid(column = 0, row = 4,columnspan=2,sticky="nsew")
        treble_slider = ctk.CTkSlider(self, from_=-100, to=100,bg_color="black", fg_color="white", command=Set_Treble)
        treble_slider.grid(column = 0, row = 5,columnspan=2,sticky="nsew")
        treble_slider.set(Treble)
        def checkbox_event():
            global EqualizerCheck
            EqualizerCheck = bool(check_var.get())
            equalizer_dict['Equalizer'] = bool(check_var.get())
            if os.path.exists(folder_path):
                with open(equalizer_path, 'w') as f:
                        json.dump(equalizer_dict, f)


        check_var = ctk.IntVar(value=0)
        checkbox = ctk.CTkCheckBox(self, text="Enable Equalizers", command=checkbox_event,
                                     variable=check_var, onvalue=1, offvalue=0)
        checkbox.grid(column = 0, row = 6,pady=4,padx=2,columnspan=3,sticky="n")
        if EqualizerCheck:
            checkbox.toggle()
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()



Equalizerbutton = ctk.CTkButton(MainFrame, text="Equalizers",fg_color="black",hover_color='grey',bg_color='#393E46',command=EqualizerWindow)
Equalizerbutton.grid(column = 0, row = 7,padx=1,pady=1,columnspan = 2,sticky="nsew")



def set_volume(volume):
    volume_level = float(volume) / 100.0
    if os.path.exists(folder_path):
        with open(file_path, 'w') as f:
                json.dump({"CurrentVol": volume}, f)
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == "ffplay.exe":
                volume.SetMasterVolume(volume_level, None)
    except Exception as e:
        print(f'VOLUME ERROR: {e}')
volume_slider = ctk.CTkSlider(MainFrame, from_=0, to=100,bg_color="black", fg_color="white", command=set_volume)
volume_slider.grid(column = 0, row = 8,padx=1,pady=1,columnspan = 2,sticky="nsew")
volume_slider.set(volume)



def entrycheck(event):
    global process
    global playing
    playing = False
    if process != None:
        try:
            subprocess.check_call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            process = None
            print('Process killed')
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with pid {process.pid}: {e}")
    videoname = VideoEntry.get()
    if 'list' in videoname:
        t = threading.Thread(target=Playlistfunc,args=(videoname,))
        t.start()
    else:
        tt = threading.Thread(target=PlaySearch,args=(videoname,))
        tt.start()


VideoEntry.bind('<Return>', entrycheck)


def KeyBindHandler():
    global StopKeySet, StopKey, SkipKeySet, SkipKey, PauseKeySet, PauseKey, ResumeKeySet, ResumeKey
    while True:
        time.sleep(0.1)
        if StopKey != None and StopKeySet:
            if keyboard.is_pressed(f'shift+{StopKey}'):
                stopfunc()
                time.sleep(0.5)
        if SkipKey != None and SkipKeySet:
            if keyboard.is_pressed(f'shift+{SkipKey}'):
                skipfunc()
                time.sleep(0.5)
        if PauseKey != None and PauseKeySet:
            if keyboard.is_pressed(f'shift+{PauseKey}'):
                Pausefunc()
                time.sleep(0.5)
        if ResumeKey != None and ResumeKeySet:
            if keyboard.is_pressed(f'shift+{ResumeKey}'):
                Resumefuncthreadstart()
                time.sleep(1)
        

class ReplayCountWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global MaxReplays
        self.geometry("300x50")
        self.title('Max Replays')
        self.entry = ctk.CTkEntry(self, placeholder_text=str(MaxReplays))
        self.entry.pack()
        def ButtonSet():
            global MaxReplays
            MaxReplays = int(self.entry.get())
        self.button = ctk.CTkButton(self, text="Set", command=ButtonSet)
        self.button.pack()
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()


def Replayhotkey():
    ReplayCountWindow()


keyboard.add_hotkey('ctrl+alt+enter', Replayhotkey)

KeyBindthread = threading.Thread(target=KeyBindHandler)
KeyBindthread.start()


def activityhandler():
    global app
    while 1:
        time.sleep(1/10)
        app.run_callbacks()



activitythread = threading.Thread(target=activityhandler)
activitythread.start()


ctk.set_appearance_mode("dark")
root.mainloop()
