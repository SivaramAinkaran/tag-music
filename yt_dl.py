
import yt_dlp
import os

def download_music(url, output_dir):
    output_dir = os.path.expanduser(output_dir)
    
    dl_options = {
        'quiet':        True,
        'no_warnings':  True,
        'format':       'bestaudio/best',
        'postprocessors': [{
            'key':            'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'paths':     {'home': output_dir},
    }

    with yt_dlp.YoutubeDL(dl_options) as ytdl:
        ytdl.download([url])

    return