# JExternalYoutubePlayer

INSTALLATION INSTRUCTIONS:

For release: 
Just extract JExternalYoutubePlayer.zip from releases and run the exe.

For Source:
Download [FFMPEG](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
Make a folder named 'ffmpeg' in the same directory the source is in.
Extract the contents of the FFMPEG zip and move the bin folder into the ffmpeg folder you made.

Download [Discord Game SDK (2.5.6)](https://dl-game-sdk.discordapp.net/2.5.6/discord_game_sdk.zip).
Make a folder called 'lib' in the same directory as the source and put the discord_game_sdk.dll in there.

Run the source.

FEATURES:

Play Song by Search - Searches youtube for a video of the specified name and plays the audio

Song Amount - Lets you choose how many videos to search & play, or if playing a playlist lets you define the number of songs to play from that playlist

Play Playlist - Allows you to play Youtube Playlists, can either use regular Youtube URLs or Youtube Music URLs.

Download - Can insert playlist URL and download whole playlist or if playing music can download the song that's currently playing

Stop, Pause, Skip & Resume buttons

Equalizers - Currently only has Bass and Treble sliders but might add the whole range later on. Be careful using this with high values.

Volume Slider

Saving - Currently the Equalizer sliders & volume slider will automatically save for you

Keybinds - Right click Stop, Pause, Skip or Resume then press any letter or number to assign it. To use keybinds hold shift then press the key you assigned

Multi Search - You can search for songs by multiple artists or search multiple keywords by seperating keywords with ':'. 

Multi Search Example: `Slipknot:System of a Down:Rage Against the Machine:Metallica:Iron Maiden`

**Audio Filters**
| Filter | Description | Set Value |
| --- | --- | --- |
| duration | Let's you set max duration of song | ✅ 1 |
| nightcore | Gives your audio a nightcore style | ❌ |
| compand | Compands your audio | ❌ |
| setrate | Sets the rate of your audio (Must use mathmatical operations)| ✅ 1 |
| reverb | Sets the reverb of your audio, first value you can set is gain, second is reverb delay | ✅ 2 |
| lofi | Gives your audio a lofi style | ❌ |
| slow | Slows your audio | ❌ |
| chiptune | Gives your audio a chiptune style | ❌ |
| bitcrush | Lets you 'crush' the bitrate of the audio | ✅ 1 |
| swirl | Gives your audio a swirl effect, first value is Swirl Delay and second value is Swirl Depth | ✅ 2 |

All filters that are able to have values set are optional and if you don't choose to set one it'll use default values.

Audio Filter Example: `Slipknot:nightcore:compand:setrate=*1.5:reverb=0.8,0.3:lofi:slow:chiptune:bitcrush=5:swirl=5:duration=5`

Search from file - Lets you search with a saved file (Such as using something as the audio filter example with a sizeable list of filters or artists). All you have to do is create a txt file named `runfile` then to run that you just type `jrunfile` into the search box and press enter. You can also make multiple of these files by adding a name to the end such as `runfilerock` and you can access that specific file using `jrunfile+rock`

