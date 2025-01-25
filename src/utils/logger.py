import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.constants import ROOT_DIR

def setup_logger(name, log_file=None, level=logging.INFO):
    """设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径（相对于ROOT_DIR/usr/logs/）
        level: 日志级别
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 清除已存在的处理器
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        log_dir = os.path.join(ROOT_DIR, 'usr', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, log_file),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# 创建默认日志记录器
upload_logger = setup_logger('upload', 'upload/upload.log')
webhook_logger = setup_logger('webhook', 'webhook/webhook.log') 