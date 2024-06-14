import os
import shutil
import instaloader
from pytube import YouTube
import re
from moviepy.editor import VideoFileClip
import subprocess

def clear_and_create_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Deleted all contents of {directory_path}")
    os.makedirs(directory_path, exist_ok=True)

def remove_hashtags(caption):
    return re.sub(r'#\S+', '', caption).strip()

def download_instagram_reel(url, download_path):
    clear_and_create_directory(download_path)
    
    L = instaloader.Instaloader()
    shortcode = url.split("/")[-2]

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        caption = post.caption  
        if caption:
            caption = remove_hashtags(caption)  
        L.download_post(post, target=download_path)
    except Exception as e:
        print(f"Failed to download the post: {e}")
        return None, None, None

    video_file = None
    print(f"Checking files in {download_path}")
    for file in os.listdir(download_path):
        print(f"Found file: {file}")
        if file.endswith(".mp4"):
            video_file = os.path.join(download_path, file)
            break

    if video_file is None:
        print("Video file not found.")
        return None, None, None

    try:
        video_clip = VideoFileClip(video_file)
        audio_file = os.path.join(download_path, f"{shortcode}.mp3")
        video_clip.audio.write_audiofile(audio_file)
        video_length = video_clip.duration 
        print(f"Audio saved to {audio_file}")
        return audio_file, caption, video_length
    except Exception as e:
        print(f"Failed to extract audio: {e}")
        return None, None, None

def download_youtube_video(url, download_path):
    clear_and_create_directory(download_path)

    data_dir = os.path.join(download_path)
    os.makedirs(data_dir, exist_ok=True)

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4').first()
        video_file = stream.download(output_path=data_dir)
        video_title = yt.title
        print(f"Downloaded video to {video_file}")
    except Exception as e:
        print(f"Failed to download the video: {e}")
        return None, None, None

    try:
        video_clip = VideoFileClip(video_file)
        audio_file = os.path.join(data_dir, f"{yt.video_id}.mp3")
        video_clip.audio.write_audiofile(audio_file)
        video_length = video_clip.duration 
        print(f"Audio saved to {audio_file}")
        return audio_file, video_title, video_length
    except Exception as e:
        print(f"Failed to extract audio: {e}")
        return None, None, None
