import base64
# import cv2
import io, os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import vertexai
from vertexai.preview.language_models import TextGenerationModel

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/creds/gradish-service-account.json"


class Image:
    def __init__(self, base64_string, filename, service_account_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path
        self.base64_string = base64_string
        self.filename = filename


    def decode_bas64_string(self):
        decoded = base64.b64decode((self.base64_string))

        image_path = f"temp/{self.filename}.jpeg"

        image_file = open(image_path, "wb")
        image_file.write(decoded)
        image_file.close()

        return image_path

    
    def enhance_image(self, image_path):
        image = cv2.imread(image_path)
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

        sharpened_image = cv2.addWeighted(blurred_image, 1.5, grayscale_image, -0.5, 0)

        enhanced_image_path = f'temp/sharpened_image_{self.filename}.jpg'
        cv2.imwrite(enhanced_image_path, sharpened_image)

        return enhanced_image_path


    def detect_handwriting(self, image_path):
        client = vision_v1.ImageAnnotatorClient()

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision_v1.types.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.text_annotations

        words = []
        for text in texts:
            words.append(text.description)
        
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

        if "mark" not in grades:
            grades["mark"] = "0"

        if "coded number" not in grades:
            grades["coded number"] = "CO123"
    

        return grades


    def extract_info(self, 
    text_array: list, 
    project_id: str,
    model_name: str,
    temperature: float,
    max_decode_steps: int,
    top_p: float,
    top_k: int,
    location: str = "us-central1",
    tuned_model_name: str = "", 
    identification=bool, 
    mark=bool):
        if identification == mark:
            return (0, 0, 0, 0)

        if mark == True:
            extract = "coded number and mark on 70"
            output_format = ("coded number", "mark on 70")

        if identification == True:
            extract = "coded number, registeration number, and name"
            output_format = '("coded number", "registeration number", "name")'

        content = f"Detect the {extract} in the following array and return it in the format: {output_format}. \n Array: {text_array}"

        vertexai.init(project=project_id, location=location)
        model = TextGenerationModel.from_pretrained(model_name)
        if tuned_model_name:
            model = model.get_tuned_model(tuned_model_name)
        response = model.predict(
            content,
            temperature=temperature,
            max_output_tokens=max_decode_steps,
            top_k=top_k,
            top_p=top_p,)
        return response.text
            

            

        
