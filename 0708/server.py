# Flask를 이용해서 값을 받아오고 저장한다. 
import csv
from flask import Flask, request

app = Flask(__name__)

CSV_FILE_PATH = '/path/to/save/loadcell_data.csv'

@app.route('/upload', methods=['POST'])
def upload():

    timestamp = request.form['timestamp']
    loadcell_value = request.form['loadcell_value']
    coner_point = request.form['coner_point']
    box_height = request.form['box_height']


    # 로드셀 값 처리
    with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([timestamp, loadcell_value, coner_point, box_height])

    return "Upload successful", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
