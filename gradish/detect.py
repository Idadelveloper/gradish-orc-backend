from google.cloud import vision_v1
import io, os
from google.cloud.vision_v1 import types


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/creds/gradish-service-account.json"
client = vision_v1.ImageAnnotatorClient()


def detect_handwriting(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    words = []
    for text in texts:
        words.append(text.description)

    return words


