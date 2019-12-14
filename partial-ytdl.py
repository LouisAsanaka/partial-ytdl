from datetime import datetime
import youtube_dl
import subprocess
import random, string
from pprint import pprint
import argparse

def subtract_time(start, end):
    FMT = '%H:%M:%S.%f'
    if '.' not in start:
        start += '.000'
    if '.' not in end:
        end += '.000'
    delta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    return str(delta)[:-3]
    
parser = argparse.ArgumentParser(description='Partial-YTDL Help')
parser.add_argument('--url', type=str, help='URL of the Youtube video')
parser.add_argument('--start', type=str, help='Start time (in seconds, or in hh:mm:ss[.xxx] form)')
parser.add_argument('--end', type=str, help='End time (in seconds, or in hh:mm:ss[.xxx] form)')
args = parser.parse_args()

url = args.url
if url is None:
    url = input('Enter URL: ')

start_time = args.start
if start_time is None:
    start_time = input('Enter start time (in seconds, or in hh:mm:ss[.xxx] form): ')
    
end_time = args.end
if end_time is None:
    end_time = input('Enter end time (in seconds, or in hh:mm:ss[.xxx] form): ')
duration = subtract_time(start_time, end_time)

ffmpeg_command = 'ffmpeg -hide_banner'

with youtube_dl.YoutubeDL({}) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    title = info_dict['title']
    formats = info_dict['requested_formats']
    for format in formats:
        format_url = format['url']
        ffmpeg_command += f' -ss "{start_time}" -i "{format_url}"'
    random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    ffmpeg_command += f' -t "{duration}" -c copy -map 0:v -map 1:a -c:v libx264 -c:a aac "{random_name}-{title}.mp4"'
    subprocess.run(ffmpeg_command)
subprocess.run("cls", shell=True)
print("Done!")
input()
