import streamlit as st
import yt_dlp
import os
import tempfile

def download_video(url):
    # Create a temporary directory to store the downloaded videos
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([url])
            return os.path.join(temp_dir, filename)

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