import os
from flask import Flask, render_template, jsonify, abort

app = Flask(__name__, static_url_path='/static')


FILES_FOLDER = os.path.join(os.getcwd(), 'static')
JSON_FOLDER = os.path.join(FILES_FOLDER, 'json_output')
CSV_FOLDER = os.path.join(FILES_FOLDER, 'csv_output')

def getFiles():
    return [os.path.splitext(f)[0] for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]


@app.route('/')
def index():
    files = getFiles() 
    return render_template('index.html', files=files )

if __name__ == '__main__':
    app.run(debug=True)
