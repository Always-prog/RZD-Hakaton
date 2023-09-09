from flask import Flask, render_template, request
import pandas as pd
import json
import stl_generator

from report_generator import get_rpz_report

app = Flask(__name__)


@app.route('/')
def index():
    materials_list = []
    with open('./materials.json', 'r') as f:
        materials_list = json.load(f)
    styles = ['styles.css']
    scripts = ['script.js', 'script_three.js']
    return render_template('index.html',
                            materials_list=materials_list,
                            styles=styles,
                            scripts=scripts)


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
    input_data = request.json
    df_data = pd.DataFrame(
        input_data[1:],
        columns=input_data[0],
        dtype=pd.Int32Dtype)
    rpz_report = get_rpz_report(df_data)
    return rpz_report


@app.route('/get_stl', methods=['POST'])
def get_stl():
    config = dict()
    with open("./размещенный_груз_и_платформы.json", "rb") as f:
        data = f.read()
        config = json.loads(data)
    data = stl_generator.create_cube_set(config)
    return data


if __name__ == '__main__':
    app.run()
