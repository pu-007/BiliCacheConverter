# Bilibili Cache File Converter

使用FFmpeg编写的一个简单的Python脚本，用于将Bilibili Windows客户端的缓存文件转换为常见的MP4文件。

A simple Python script using ffmpeg to cover cache files of Bilibili's Windows client into common MP4 files.

# Requires

1. FFmpeg
2. Python 3
3. BiliBili Windows client

## Usage

将BILI_FOLDER全局变量设置为main.py中的您自己的值，然后运行代码。

Set the `BILI_FOLDER` global variable to your own value in `main.py`, and run the code.

视频将存储在位于工作目录中的"output"文件夹中。

The videos will be stored in the "output" folder located in the working directory.

```python
...
if __name__ == "__main__":
    # Replace "your_value" with the desired folder path
    BILI_FOLDER = r"your value" 
    ...
```

如果你想转换某一个视频，你可以使用 merge_video 函数。

If you want to cover specific video, you can use the `merge_video` function.

```python
def merge_video(video_folder: Path) -> None:
    ...
```
