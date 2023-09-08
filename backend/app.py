from flask import Flask, render_template, request
from flask import jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        data = request.json
        print(data)
        return jsonify({'message': "OK"})
    else:
        return render_template("result.html")


if __name__ == '__main__':
    app.run()
