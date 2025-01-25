import os
from pathlib import Path

SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
ROOT_DIR = str(Path(SRC_DIR).parent)
VIDEOS_DIR = os.path.join(ROOT_DIR, 'usr', 'brec') # base path for videos, + RelativePath (e.g. '/viddeos/xxx')
# 短视频存储目录
SHORT_VIDEOS_DIR = os.path.join(ROOT_DIR, 'usr', 'short_videos')
