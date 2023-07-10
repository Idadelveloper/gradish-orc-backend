from flask import Flask, jsonify, request
from gradish.image import Image
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/extract", methods=['POST'])
def extract_info():
    request_data = request.get_json()
    base64_string = request_data['base64_string']
    filename = request_data['filename']
    service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')

    image = Image(base64_string, filename, service_account_path)

    image_path = image.decode_bas64_string()
    text = image.detect_handwriting(image_path)

    final = image.extract_info(text, os.getenv("PROJECT_ID"), os.getenv("MODEL_NAME"), 0.2, 256, 0.8, 40, mark=True, identification=False)
    
    grades = dict()
    for i in range(len(words)):
        if words[i] == "NUMBER":
            coded_number = words[i + 1]
            cn_re = '[A-Za-z0-9]+'
            grades['coded number'] = coded_number

        if words[i] == "Total":
            mark = words[i-1]
            grades['mark'] = mark
            break
    print(grades)

    return jsonify(grades), 200

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)

