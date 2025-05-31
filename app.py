import logging
from utils.path_util import get_script_absolute_path
import os
from flask import Flask, request, send_from_directory, jsonify, render_template

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
UPLOAD_FOLDER = get_script_absolute_path(__file__, 'storage')
logging.info(f'UPLOAD_FOLDER: {UPLOAD_FOLDER}')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 100 MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def upload_form():
    """显示文件上传页面"""
    # 获取已上传的文件列表（只显示最近10个）
    try:
        files = sorted(os.listdir(app.config['UPLOAD_FOLDER']),
                       key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)),
                       reverse=True)[:10]
    except Exception as e:
        logging.error(f"获取文件列表失败: {e}")
        files = []

    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    """上传大文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    logging.info(f'成功接受上传的文件: {file.filename}')
    logging.info('保存中...........')
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        with open(file_path, 'wb') as f:
            while True:
                chunk = file.stream.read(4096)
                if not chunk:
                    break
                f.write(chunk)

        download_link = f'http://{request.host}/download/{file.filename}'
    except Exception as e:
        logging.error(f'保存文件时出错: {e}')
        return jsonify({'error': '保存文件失败'}), 500
    return jsonify({
        'message': f'文件 {file.filename} 上传成功',
        'download_link': download_link
    }), 200


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
                    logging.info(f'已删除文件: {file_path}')
            except Exception as e:
                logging.error(f'删除文件时出错: {file_path}, 错误信息: {e}')
    else:
        logging.warning(f'目录不存在: {directory}')


if __name__ == '__main__':
    # 启动定时任务线程
    # scheduler_thread = threading.Thread(target=run_schedule)
    # scheduler_thread.daemon = True
    # scheduler_thread.start()

    # 启动Flask应用
    app.run(host='0.0.0.0', port=10000, debug=True)