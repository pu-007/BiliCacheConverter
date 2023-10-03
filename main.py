from pathlib import Path
from json import load 
import os
import subprocess
import re

OUTPUT_FOLDER = Path("output")
TEMP_FOLDER = Path("temp")

def auto_mkdir(dir_name: Path):
    # create a dir if it doesn't exist
    if not dir_name.exists():
        dir_name.mkdir()

auto_mkdir(OUTPUT_FOLDER)
auto_mkdir(TEMP_FOLDER)

def remove_mask(input, output):
    # read binary input_path file, and remove bytes 0-9, finally write to output_path
    # Read a binary file from input_path
    # emove the bytes with values from 0 to 8
    # (The first nine digits are all zeros.)
    # and finally write it to output_path
    with open(input, "rb") as f:
        data = f.read()
    with open(output, "wb") as f:
        f.write(data[9:])
    # close file
    f.close()

def replaze_windows_illegal_char(input: str) -> str:
    # replace windows illegal char with '_'
    # https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
    return re.sub(r'[\\/:*?"<>|]', "_", input)

def recognize_file_type(input) -> str | None:
    # use ffmpeg to recognize the input file has audio or video track
    cmd = f'ffmpeg -i "{input}"'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, shell=True)
    output = result.stderr.decode('utf-8')
    # video track should be checked at first
    # as if it's a video file
    #   it may be mistakenly identified as an audio file
    #   if we check audio track first
    if 'Video' in output: # for Video only or Video + Audio
        return "mp4"
    if 'Audio' in output: # for Video only
        return "mp3"
    else: # for others
        return None

def get_track_title(video_folder):
    track_info = load(Path(video_folder, ".videoinfo").open("r", encoding="utf-8"))
    return track_info["title"]

def find_tracks(video_folder) -> tuple:
    audio, video = None, None
    for track in video_folder.glob("*.m4s"):
        real_track = TEMP_FOLDER / f"{track.name}.temp"
        remove_mask(track, real_track)
        track_type = recognize_file_type(real_track)
        if track_type == "mp3":
            audio = real_track
        elif track_type == "mp4":
            video = real_track
    return audio, video

def count_folders(path):
    p = Path(path)
    return len([f for f in p.iterdir() if f.is_dir()])


def merge_video(video_folder: Path) -> None:
    title = get_track_title(video_folder) + ".mp4"
    print(f"Processing -- {title}...")
    audio, video = find_tracks(video_folder)
    if audio is None or video is None:
        print(f"\tError: {video_folder} is not a valid video folder")
    else:
        os.system(f'ffmpeg -loglevel quiet -i "{audio}" -i "{video}"\
                    -c:v copy -c:a aac -strict experimental \
                    "{OUTPUT_FOLDER / replaze_windows_illegal_char(title)}"')
        # remove temp audio and video track
        os.remove(audio)
        os.remove(video)

def process(bili_folder: Path):
    # Use a 'for loop' to iterate over all the 'folders' in 'bili_folder'
    for current, video_folder in enumerate(bili_folder.iterdir()):
        if not video_folder.is_dir():
            continue
        print( f"[{current+1}/{count_folders(bili_folder)}][{video_folder.name}]",
            end = " ")
        merge_video(video_folder)

if __name__ == "__main__":
    BILI_FOLDER = r"D:\Videos\bilibili"
    process(bili_folder=Path(BILI_FOLDER))
