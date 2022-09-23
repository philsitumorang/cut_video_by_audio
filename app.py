import moviepy.editor as mp


video = mp.VideoFileClip("digitakt-dark-elektro-2-fin.mp4")
video.audio.write_audiofile("output.mp3")