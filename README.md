# cut_video_by_audio
Cut video if an audio threshold is very low.

### How to add video files
Create list.txt and add to the file path to video.
file 'build/0.mp4'
file 'build/1.mp4'

### How to run the application
python3 app.py
1. This app collects all files from list.txt
2. Skip all quiet moments and merge all files in one.

### How to setup config
Open trim.py

    VIDEOFILE_NAME = "video" 
    OUTPUT_FILE = "output.mp4"
    OUTPUT_BITRATE = "5000k" - You can change a bitrate to increase or decrease the quality of your video.
    DIR = 'build' - Directory where you store your video files.
    MS = 100 - Every 100ms script checks the volume level, you can change it and find the optimal parameter. This param will be affected by the result.
    AUDIO_THRESHOLD = -30 - If you change this value you can find the optimal frame range that the script must remove.
    FRAME_THRESHOLD = 7 - This value defines the difference between frames. If frames are similar that means this part of the video is empty/frozen.
