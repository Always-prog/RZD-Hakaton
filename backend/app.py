from flask import Flask, render_template, request
from flask import jsonify

from report_generator import get_rpz_report

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', show_files=False)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        try:
            data = request.json
            print(data)
            return jsonify({'message': "OK"}), 200
        except:
            raise ValueError()
    else:
        return render_template("result.html")


@app.route('/download/file1', methods=['POST'])
def download_file1():
    input_data = request.json
    print(input_data)
    data = None
    with open('./files/file_10074349_signed.pdf', 'rb') as f:
        data = f.read()
    return data


@app.route('/download/file2', methods=['POST'])
def download_file2():
    input_data = request.json
    print(input_data)

    rpz_report = get_rpz_report(input_data)

    return rpz_report


if __name__ == '__main__':
    app.run()
