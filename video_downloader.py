import streamlit as st
import yt_dlp
import os
import subprocess

def download_video(url):
    # Create a directory to store the downloaded videos
    download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title).50s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        full_path = os.path.join(download_dir, filename)
        ydl.download([url])

        # Use the ffmpeg command-line tool to ensure the video is in the correct format
        subprocess.run(['ffmpeg', '-i', full_path, '-c', 'copy', '-f', 'mp4', full_path])

        if os.path.exists(full_path):
            return full_path
        else:
            raise FileNotFoundError(f"Failed to download the video to {full_path}")

st.title("Video Downloader")

url = st.text_input("Enter the video URL:")

if st.button("Download"):
    try:
        filename = download_video(url)
        st.success(f"Download complete! The video is saved as {os.path.basename(filename)}")
        with open(filename, "rb") as file:
            st.download_button(
                label="Download Video",
                data=file,
                file_name=os.path.basename(filename),
                mime="video/mp4",
            )
    except Exception as e:
        st.error(f"Error downloading the video: {e}")