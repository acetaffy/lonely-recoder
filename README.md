# 孤独录播

轻量的录播脚本，自动录制 bilibili 直播并投稿至 bilibili

## Why

- 轻量，占用极小的存储
- 专注于录播上传，无其他功能
- 即上传即删除，5GB 存储服务器也可轻松使用

## Usage

**Step 1**

```bash
git clone https://github.com/acetaffy/lonely-recoder
cd lonely-recoder
```

**Step 2**

```bash
pip install -r requirements.txt
```

**Step 3**

```bash
./upload.sh
./record.sh
```

访问 http://0.0.0.0:23560 使用 BililiveRecorder WebUI

使用 `./stop.sh` 停止所有任务

## Credits

- [timerring/bilive](https://github.com/timerring/bilive) 基于此项目修改
- [BililiveRecorder/BililiveRecorder](https://github.com/BililiveRecorder/BililiveRecorder) - [GPL-3.0 license](https://github.com/BililiveRecorder/BililiveRecorder#GPL-3.0-1-ov-file)
- [biliup/biliup-rs](https://github.com/biliup/biliup-rs) - [MIT license](https://github.com/biliup/biliup-rs#MIT-1-ov-file), 项目内包含闭源二开版本
- [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) - [LICENSE](https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md)

 