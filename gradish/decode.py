import base64
import tempfile


def decode_image(base64_string, img_name):
    decoded = base64.b64decode((base64_string))

    image_path = f"temp/{img_name}.jpeg"

    image_file = open(image_path, "wb")
    image_file.write(decoded)
    image_file.close()

    return image_path

    


