from PIL import ImageFilter
from PIL.Image import Image
from ktpocr.ocr import get_text_area

def preprocess(img: Image, treshold = 150) -> Image:
    img = img.convert("L")
    # img = get_text_area(img)
    img = img.filter(ImageFilter.MedianFilter)
    img = img.point(lambda x: 255 if x > treshold else 0)

    return img