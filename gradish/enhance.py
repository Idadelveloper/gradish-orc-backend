import cv2


def enhance_image(image_path):
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
    sharpened_image = cv2.addWeighted(blurred_image, 1.5, grayscale_image, -0.5, 0)
    cv2.imwrite("temp/sharpened_image.jpg", sharpened_image)

    return