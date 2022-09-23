import os
import shutil
import moviepy.editor as mp
import numpy as np

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import concatenate_videoclips
from pydub import AudioSegment
from pprint import pprint


def init():
    VIDEOFILE_NAME = "video"
    OUTPUT_FILE = "output.mp4"
    OUTPUT_BITRATE = "5000k"
    DIR = 'build'
    MS = 100
    AUDIO_THRESHOLD = -30
    FRAME_THRESHOLD = 7

    if os.path.exists(DIR):
        shutil.rmtree(DIR)

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    video = mp.VideoFileClip(f"{VIDEOFILE_NAME}.mp4")
    # video = video.subclip(0, 20)
    video.audio.write_audiofile(f"{VIDEOFILE_NAME}.mp3")

    sound = AudioSegment.from_mp3(f'{VIDEOFILE_NAME}.mp3')
    LAST_MS = int(len(sound))

    time_dict = {}
    time_index = 0
    frame_list = []

    DURATION_LIST = list(range(0, LAST_MS + 1, MS))
    for index, ms in enumerate(DURATION_LIST):
        if len(DURATION_LIST) - 1 <= index:
            break

        if not time_dict.get(time_index):
            time_dict[time_index] = []

        dBFS = sound[ms:DURATION_LIST[index + 1]].dBFS

        if dBFS > AUDIO_THRESHOLD:
            for frame_index, frame in enumerate(frame_list):
                if frame_index < len(frame_list) - 1:
                    before = np.array(frame_list[frame_index]['frame'])
                    now = np.array(frame_list[frame_index + 1]['frame'])
                    diff = np.mean((now - before) ** 2)
                    if diff > FRAME_THRESHOLD:
                        if not time_dict.get(time_index):
                            time_dict[time_index] = []
                        if len(time_dict[time_index]) > 0 and frame['time'] - time_dict[time_index][-1:][0][1] > 1:
                            time_index += 1
                            print(f"time_index: {time_index}")
                        else:
                            time_dict[time_index].append((frame['time'], frame_list[frame_index + 1]['time']))

            frame_list = []

            if not time_dict.get(time_index):
                time_dict[time_index] = []

            print(f"SHIIIIIT - {len(time_dict[time_index])}; {time_dict[time_index]};")
            if len(time_dict[time_index]) > 0 and ms / 1000 - time_dict[time_index][-1:][0][1] > 2:
                time_index += 1
            else:
                time_dict[time_index].append((ms / 1000, DURATION_LIST[index + 1] / 1000))
        else:
            frame = video.get_frame(DURATION_LIST[index + 1] / 1000)
            frame_list.append({
                'frame': frame,
                'time': DURATION_LIST[index + 1] / 1000,
                'dBFS': dBFS
            })

    for frame_index, frame in enumerate(frame_list):
        if frame_index < len(frame_list) - 1:
            before = np.array(frame_list[frame_index]['frame'])
            now = np.array(frame_list[frame_index + 1]['frame'])
            diff = np.mean((now - before) ** 2)
            if diff > FRAME_THRESHOLD:
                if not time_dict.get(time_index):
                    time_dict[time_index] = []
                if len(time_dict[time_index]) > 0 and frame['time'] - time_dict[time_index][-1:][0][1] > 1:
                    time_index += 1
                    print(f"time_index: {time_index}")
                else:
                    time_dict[time_index].append((frame['time'], frame_list[frame_index + 1]['time']))

    pprint("---- SEPARATED TIMELINE ----")
    pprint(time_dict)

    time_list = []
    for key in time_dict:
        first = time_dict[key][0][0]
        last = time_dict[key][-1:][0][1]
        time_list.append((first, last))

    pprint("---- PREPARED TIMELIST ----")
    pprint(time_list)

    video_list = []
    for index, time in enumerate(time_list):
        print(f"time 0: {time[0]}; time 1: {time[1]}")
        clip = video.subclip(time[0], time[1])
        clip = clip.audio_fadein(0.01).audio_fadeout(0.01)
        new_video = clip.set_audio(clip.audio)
        video_list.append(new_video)

    final_clip = concatenate_videoclips(video_list)
    final_clip.write_videofile(OUTPUT_FILE, bitrate=OUTPUT_BITRATE)

init()
