import streamlit as st
import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title).50s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        ydl.download([url])
    return filename

st.title("Video Downloader")

url = st.text_input("Enter the video URL:")

if st.button("Download"):
    try:
        filename = download_video(url)
        st.success(f"Download complete! The video is saved as {filename}")
        with open(filename, "rb") as file:
            st.download_button(
                label="Download Video",
                data=file,
                file_name=filename,
                mime="video/mp4",
            )
    except Exception as e:
        st.error(f"Error downloading the video: {e}")