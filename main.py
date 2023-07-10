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
def extract_mark():
    request_data = request.get_json()
    base64_string = request_data['base64_string']
    filename = request_data['filename']
    service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')

    image = Image(base64_string, filename, service_account_path)

    image_path = image.decode_bas64_string()
    text = image.detect_handwriting(image_path)

    data = {'detected': text}
    print(data)

    return jsonify(data), 200


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)

