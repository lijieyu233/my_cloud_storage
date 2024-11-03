import threading

from flask import Flask, request, send_from_directory, jsonify
import os

from logger_setup import setup_logger
from path_util import get_script_absolute_path

logger=setup_logger(__name__)
app = Flask(__name__)
UPLOAD_FOLDER = get_script_absolute_path(__file__,'storage')
logger.info(f'UPLOAD_FOLDER: {UPLOAD_FOLDER}')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 创建上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return '没有文件', 400
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    download_link = f'http://127.0.0.1:10000/download/{file.filename}'
    return jsonify({'message': f'文件 {file.filename} 上传成功', 'download_link': download_link}), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """下载文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def delete_files_in_directory(directory):
    """删除指定目录中的所有文件。"""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f'已删除文件: {file_path}')
            except Exception as e:
                logger.error(f'删除文件时出错: {file_path}, 错误信息: {e}')
    else:
        logger.warning(f'目录不存在: {directory}')

def job():
    """调度任务，每天零点执行删除操作。"""
    delete_files_in_directory(app.config['UPLOAD_FOLDER'])

# 每天零点执行 job 函数
# schedule.every().day.at("00:00").do(job)

def run_schedule():
    """在单独线程中运行调度器。"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次
if __name__ == '__main__':
    app.run(port=10000,debug=True)
    threading.Thread(target=run_schedule,daemon=True).start()