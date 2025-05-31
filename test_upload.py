import requests

def upload_file(file_path):
    url = 'http://117.72.36.222:10000/upload'  # 替换为您的 Flask 服务器地址
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        return response.json()

if __name__ == '__main__':
    file_path = 'D:\用户\视频\Elden Ring/弹反处决熔炉骑士.mp4'.replace("\\", "/")
    result = upload_file(file_path)
    print(result)
