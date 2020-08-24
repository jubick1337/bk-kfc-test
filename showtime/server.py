import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/points', methods=['GET'])
def some():
    with open('../results/result.geojson') as data_file:
        data = data_file.read()
        data_content = json.loads(data)
    return data_content


@app.route('/')
def main():
    return render_template('./page.html')


app.run()
