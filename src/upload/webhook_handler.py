import threading
from pathlib import Path
import os
import asyncio
from src.constants import VIDEOS_DIR
from quart import Quart, request, jsonify
from src.utils.logger import webhook_logger

app = Quart(__name__)

@app.route('/webhook', methods=['POST'])
async def handle_webhook():
    data = await request.get_json()
    webhook_logger.info(f"收到webhook请求: {data['EventType']}")
    
    # 只处理文件关闭事件
    if data['EventType'] == 'FileClosed':
        event_data = data['EventData']
        file_path = Path(VIDEOS_DIR) / event_data['RelativePath']
        
        webhook_logger.info(f"处理文件关闭事件: {file_path}")
        
        if file_path.exists() and file_path.suffix.lower() in ['.flv', '.mp4']:
            from src.upload.upload import pre_upload
            s_file_path = str(file_path)
            webhook_logger.info(f"文件符合要求，加入上传队列: {s_file_path}")
            # 在新的事件循环中异步处理上传
            asyncio.create_task(async_pre_upload(s_file_path))
            return jsonify({'status': 'success', 'message': '文件已加入处理队列'}), 200
        else:
            webhook_logger.warning(f"文件不存在或格式不支持: {file_path}")
    
    return jsonify({'status': 'success', 'message': '事件已接收'}), 200

async def async_pre_upload(file_path):
    """
    异步包装pre_upload函数
    """
    from src.upload.upload import pre_upload
    try:
        # 在线程池中执行阻塞操作
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, pre_upload, file_path)
    except Exception as e:
        webhook_logger.error(f"处理上传时发生错误: {str(e)}")

async def run_webhook_server(host='0.0.0.0', port=18861):
    """
    启动 webhook 服务器
    """
    webhook_logger.info(f"Webhook服务器正在启动，监听地址：{host}:{port}")
    if os.environ.get('FLASK_ENV') == 'development':
        await app.run_task(host=host, port=port)
    else:
        # 在生产环境中使用 hypercorn
        import hypercorn.asyncio
        import hypercorn.config

        config = hypercorn.config.Config()
        config.bind = [f"{host}:{port}"]
        
        webhook_logger.info("使用hypercorn启动webhook服务器")
        await hypercorn.asyncio.serve(app, config)

