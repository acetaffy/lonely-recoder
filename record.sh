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
LOG_DIR="$CURRENT_PATH/usr/logs/brec"
mkdir -p "$LOG_DIR"

# 生成日志文件名
LOG_FILE="$LOG_DIR/brec-$(date +%Y%m%d-%H%M%S).log"

export BILILIVERECORDER_LOG_FILE_PATH="$LOG_DIR/"

# bind host and port (can edit)
host=0.0.0.0
port=23560
user=root
pass=root

log "INFO" "正在停止旧的BililiveRecorder进程..."
kill -9 $(pgrep -f brec) 2>/dev/null || true

log "INFO" "启动BililiveRecorder..."
nohup ./src/bin/brec/BililiveRecorder.Cli run \
    --bind "http://$host:$port" \
    --http-basic-user "$user" \
    --http-basic-pass "$pass" \
    "$CURRENT_PATH/usr/brec" >/dev/null 2>&1 &

# 检查进程是否成功启动
sleep 2
if pgrep -f brec > /dev/null; then
    log "INFO" "BililiveRecorder启动成功！"
    log "INFO" "日志文件位置: $LOG_FILE"
else
    log "ERROR" "BililiveRecorder启动失败！"
    log "ERROR" "请检查日志文件: $LOG_FILE"
    exit 1
fi

