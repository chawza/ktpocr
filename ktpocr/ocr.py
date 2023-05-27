from pytesseract import image_to_string
from PIL import Image

def ocr_tesseract(img: Image):
    return image_to_string(img)
