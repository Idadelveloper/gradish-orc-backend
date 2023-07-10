from flask import Flask, jsonify, request
from gradish.image import Image
import base64
import os
import uuid
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.data)
    
    uploaded_file = request.data
    # Save the uploaded file to a new file in the root directory

    with open('myimage', 'wb') as f:
        # Write some bytes to the file
        f.write(uploaded_file)

    with open('myimage', 'rb') as f:
        file_contents = f.read()  
        
        # Encode the binary data as base64
        base64_string = base64.b64encode(file_contents).decode('utf-8')
        
        print(request.headers)
        content_type = request.content_type.split("/")[1]
        filename = f"_gradish_image_{uuid.uuid4()}.{content_type}"
        service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')

        image = Image(base64_string, filename, service_account_path)

        image_path = image.decode_bas64_string()
        text = image.detect_handwriting(image_path)

        data = {'detected': text}
        print(data)

        return jsonify(data), 200
    
    return 'File saved successfully', 200


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

