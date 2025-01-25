#!/bin/bash

# 使用说明：
# 1. 给脚本添加执行权限：
#    chmod +x src/utils/clearLogs.sh
#
# 2. 直接运行脚本：
#    ./src/utils/clearLogs.sh
#
# 3. 添加到crontab定时执行（例如每天凌晨2点）：
#    0 2 * * * /path/to/src/utils/clearLogs.sh
#
# 说明：脚本会自动清理指定目录下超过7天的.log文件和.gz文件
# 如需修改保留天数，请修改下方find命令中的 mtime +7 参数

# 定义日志目录
LOG_DIRS=("/usr/logs" "/src/brec/logs")

# 获取当前时间戳
current_timestamp=$(date +%s)

# 设置日志保留时间（7天，单位：秒）
retention_period=$((7 * 24 * 60 * 60))

# 遍历所有日志目录
for dir in "${LOG_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "正在清理目录: $dir"
        
        # 查找并删除7天前的日志文件
        find "$dir" -type f -name "*.log" -mtime +7 -exec rm -f {} \;
        
        # 查找并删除7天前的gz压缩文件
        find "$dir" -type f -name "*.gz" -mtime +7 -exec rm -f {} \;
        
        echo "清理完成: $dir"
    else
        echo "警告: 目录不存在 - $dir"
    fi
done

echo "所有日志清理任务已完成"
