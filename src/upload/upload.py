import subprocess
import os
import time
import shutil
import asyncio
from src.constants import SRC_DIR, ROOT_DIR, SHORT_VIDEOS_DIR
from datetime import datetime
from src.upload.generate_yaml import generate_yaml_template
from src.upload.extract_video_info import generate_title, get_video_duration
from src.upload.webhook_handler import run_webhook_server
from src.utils.logger import upload_logger

def upload_video(upload_path, yaml_file_path):
    try:
        # Construct the command
        command = [
            f"{ROOT_DIR}/src/bin/biliup",
            "-u",
            f"{ROOT_DIR}/usr/cookies.json",
            "upload",
            upload_path,
            "--extra-fields",
            "{\"is_only_self\":1}",
            "--config",
            yaml_file_path
        ]
        
        upload_logger.info(f"开始上传视频: {upload_path}")
        upload_logger.debug(f"上传命令: {' '.join(command)}")
        
        # Execute the command
        result = subprocess.run(command, check=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            upload_logger.info(f"视频上传成功，准备删除源文件: {upload_path}")
            os.remove(upload_path)
        else:
            upload_logger.error(f"上传失败，文件将被删除: {upload_path}")
            os.remove(upload_path)
            return False
    
    except subprocess.CalledProcessError as e:
        upload_logger.error(f"上传过程发生错误: {str(e)}")
        upload_logger.error(f"文件将被保留: {upload_path}")
        return False
    except Exception as e:
        upload_logger.exception(f"发生未预期的错误: {str(e)}")
        return False

def find_bv_number(target_str, my_list):
    for element in my_list:
        if target_str in element:
            parts = element.split('\t')
            if len(parts) > 0:
                return parts[0]
    return None

def pre_upload(upload_video_path):
    try:
        upload_logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 处理文件: {upload_video_path}")
        
        # 检查视频时长
        duration = get_video_duration(upload_video_path)
        if duration is not None and duration < 300:  # 小于5分钟
            # 确保短视频目录存在
            os.makedirs(SHORT_VIDEOS_DIR, exist_ok=True)
            # 移动到短视频目录
            short_video_path = os.path.join(SHORT_VIDEOS_DIR, os.path.basename(upload_video_path))
            try:
                shutil.move(upload_video_path, short_video_path)
                upload_logger.info(f"视频时长小于5分钟，已移动到短视频目录: {short_video_path}")
                return
            except Exception as e:
                upload_logger.error(f"移动视频文件失败: {str(e)}")
                return False
        
        # 视频时长正常，继续上传流程
        query = generate_title(upload_video_path)
        result = subprocess.check_output(f"{ROOT_DIR}/src/bin/biliup" + " -u " + f"{ROOT_DIR}/usr/cookies.json" + " list", shell=True)
        upload_list = result.decode("utf-8").splitlines()
        limit_list = upload_list[:30]
        bv_result = find_bv_number(query, limit_list)
        if bv_result:
            upload_logger.info(f"BV号: {bv_result}")
            append_upload(upload_video_path, bv_result)
        else:
            upload_logger.info("首次上传该直播")
            # generate the yaml template
            yaml_template = generate_yaml_template(upload_video_path)
            yaml_file_path = SRC_DIR + "/upload/upload.yaml"
            with open(yaml_file_path, 'w', encoding='utf-8') as file:
                file.write(yaml_template)
            upload_video(upload_video_path, yaml_file_path)
            return
                
    except subprocess.CalledProcessError:
        upload_logger.error("上传失败，文件将被保留")
        return False

def append_upload(upload_path, bv_result):
    try:
        # Construct the command
        command = [
            f"{ROOT_DIR}/src/bin/biliup",
            "-u",
            f"{ROOT_DIR}/usr/cookies.json",
            "append",
            "--extra-fields",
            "{\"is_only_self\":1}",
            "--vid",
            bv_result,
            upload_path
        ]
        # Execute the command
        result = subprocess.run(command, check=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            upload_logger.info("上传成功，准备删除源文件")
            os.remove(upload_path)
        else:
            upload_logger.error("上传失败，文件将被删除")
            os.remove(upload_path)
            return False
    
    except subprocess.CalledProcessError:
        upload_logger.error("上传失败，文件将被保留")
        return False

if __name__ == "__main__":
    # 启动 webhook 服务器
    try:
        upload_logger.info("正在启动主程序...")
        asyncio.run(run_webhook_server())
    except KeyboardInterrupt:
        upload_logger.info("收到中断信号，正在关闭服务器...")
    except Exception as e:
        upload_logger.error(f"服务器运行时发生错误: {str(e)}")
        raise