import zipfile
from io import BytesIO

from flask import Flask, render_template, request
import pandas as pd
import json

from platforms_stuff import parse_cargos
from report_generator import get_rpz_reports

app = Flask(__name__)


@app.route('/')
def index():
    materials_list = []
    with open('./materials.json', 'r') as f:
        materials_list = json.load(f)
    return render_template('index.html', materials_list=materials_list)


@app.route('/download/download_scheme', methods=['POST'])
def download_scheme():
    input_data = request.json
    print(input_data)
    data = None
    with open('./files/file_10074349_signed.pdf', 'rb') as f:
        data = f.read()
    return data


@app.route('/download/download_RPZ', methods=['POST'])
def download_RPZ():
    cargos = parse_cargos(request.json)
    rpz_report = get_rpz_reports(cargos)

    zip_buffer = BytesIO()
    zip_buffer.seek(0)
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in [(f'№{i}-РПЗ-Вагон.pdf', file) for i, file in enumerate(rpz_report)]:
            zip_file.writestr(file_name, data)

    return zip_buffer.getvalue()


if __name__ == '__main__':
    app.run()
