#!/bin/bash

# 设置日志函数
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message"
}

# 停止BililiveRecorder服务
log "INFO" "正在停止BililiveRecorder服务..."
kill -9 $(pgrep -f brec) 2>/dev/null || true

# 停止上传服务
log "INFO" "正在停止上传服务..."
kill -9 $(pgrep -f src.upload.upload) 2>/dev/null || true
kill -9 $(pgrep -f biliup) 2>/dev/null || true

# 检查服务是否已经完全停止
sleep 2

# 检查BililiveRecorder
if pgrep -f brec > /dev/null; then
    log "ERROR" "BililiveRecorder服务未能完全停止！"
else
    log "INFO" "BililiveRecorder服务已停止"
fi

# 检查上传服务
if pgrep -f src.upload.upload > /dev/null || pgrep -f biliup > /dev/null; then
    log "ERROR" "上传服务未能完全停止！"
else
    log "INFO" "上传服务已停止"
fi 
