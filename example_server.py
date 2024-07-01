# Flask를 이용해서 값을 받아오고 저장한다. 

from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return "No photo part", 400

    file = request.files['photo']
    timestamp = request.form['timestamp']
    loadcell_value = request.form['loadcell_value']

    # 파일 저장
    file.save(f'/path/to/save/{timestamp}.jpg')

    # 로드셀 값 처리
    with open(f'/path/to/save/{timestamp}_loadcell.txt', 'w') as f:
        f.write(loadcell_value)

    return "Upload successful", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
