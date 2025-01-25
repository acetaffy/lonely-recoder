#!/bin/bash

# 设置日志函数
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 确保日志目录存在
CURRENT_PATH=$(pwd)
LOG_DIR="$CURRENT_PATH/usr/logs/upload"
mkdir -p "$LOG_DIR"

# 生成日志文件名
LOG_FILE="$LOG_DIR/upload-$(date +%Y%m%d-%H%M%S).log"

# 停止旧的进程
log "INFO" "正在停止旧的上传进程..."
kill -9 $(pgrep -f src.upload.upload) 2>/dev/null || true
kill -9 $(pgrep -f biliup) 2>/dev/null || true

# 启动webhook服务器
log "INFO" "启动上传服务器..."
nohup python3 -m src.upload.upload >/dev/null 2>&1 &

# 检查进程是否成功启动
sleep 2
if pgrep -f src.upload.upload > /dev/null; then
    log "INFO" "上传服务器启动成功！"
    log "INFO" "日志文件位置: $LOG_FILE"
else
    log "ERROR" "上传服务器启动失败！"
    log "ERROR" "请检查日志文件: $LOG_FILE"
    exit 1
fi
