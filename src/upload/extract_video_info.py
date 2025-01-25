import subprocess
import re
import json
import os
from datetime import datetime
from src.constants import ROOT_DIR

def get_video_info(video_file_path):
    """get the title, artist and date of the video file via ffprobe
    Args:
        video_file_path: str, the path of the video file
    Returns:
        str: the title of the video file, if failed, return None
    """
    command = [
        f"{ROOT_DIR}/src/bin/ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        video_file_path
    ] # 其实可以不用ffprobe的
    output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
    parsed_output = json.loads(output)
    title_value = parsed_output["format"]["tags"]["Title"]
    artist_value = parsed_output["format"]["tags"]["Name"]
    date_value = parsed_output["format"]["tags"]["StartTime"]
    if len(date_value) > 8:
        dt = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        new_date = dt.strftime('%Y%m%d')
    else:
        new_date = date_value
    print(title_value, artist_value, new_date)
    return title_value, artist_value, new_date

def generate_title(video_path):
    title, artist, date = get_video_info(video_path)
    new_title = artist + "直播回放-" + date + "-" + title
    return new_title

def generate_desc(video_path):
    title, artist, date = get_video_info(video_path)
    source_link = generate_source(video_path)
    new_desc = artist + "直播回放\n看得开心。"
    return new_desc

def generate_tag(video_path):
    title, artist, date = get_video_info(video_path)
    artist_text = re.sub(r'\W+', '', artist)
    tags = f"{artist_text},直播回放,直播录像"
    return tags

def generate_source(video_path):
    file_name = os.path.basename(video_path)
    match_result = re.search(r'录制-(\d+)-', file_name)
    if match_result:
        part_before_underscore = match_result.group(1)
        source_link = "https://live.bilibili.com/" + part_before_underscore
        return source_link
    else:
        return None

def get_video_duration(video_file_path):
    """获取视频时长（秒）
    Args:
        video_file_path: str, 视频文件路径
    Returns:
        float: 视频时长（秒），如果获取失败返回None
    """
    try:
        command = [
            f"{ROOT_DIR}/src/bin/ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_file_path
        ]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
        parsed_output = json.loads(output)
        duration = float(parsed_output["format"]["duration"])
        return duration
    except (subprocess.CalledProcessError, KeyError, ValueError) as e:
        print(f"获取视频时长失败: {str(e)}")
        return None

if __name__ == "__main__":
    video_path = ""
    video_title = generate_title(video_path)
    print(video_title)
    video_desc = generate_desc(video_path)
    print(video_desc)
    video_tag = generate_tag(video_path)
    print(video_tag)
    video_source = generate_source(video_path)
    print(video_source)