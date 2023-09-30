# Bilibili Cache File Converter

A simple Python script using ffmpeg to cover cache files of Bilibili's Windows client into common MP4 files.

# Requires

1. FFmpeg
2. Python 3
3. BiliBili Windows client

## Usage

Set the `BILI_FOLDER` global variable to your own value in `main.py`, and run the code.
```python
...

if __name__ == "__main__":
    # Replace "your_value" with the desired folder path
    BILI_FOLDER = r"your value" 
    ...
```

If you want to cover specific video, you can use the `merge_video` function.

```python
def merge_video(video_folder: Path) -> None:
    ...
```
