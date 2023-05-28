from pytesseract import image_to_string, image_to_boxes, Output, image_to_data
from PIL.Image import Image
from PIL import ImageDraw

def crop_text_area(img: Image) -> Image:
    result = image_to_boxes(img, output_type=Output.DICT)

    # First index is whole text
    left = result['left'][0]
    top = result['top'][0]
    right = result['right'][0]
    bottom = result['bottom'][0]

    # draw = ImageDraw.Draw(img)
    # shape = ((left,top), (right, bottom))
    # draw.rectangle(shape, outline='red', width=2)
    # img.save('test_clean_draw.jpeg')
    # raise 'asd'

    # left, upper, right, lower
    coordinte = (left, top, right, bottom)
    cropped =  img.crop(coordinte)

    width =  img.size[0]
    height = cropped.size[1] * width / cropped.size[0]
    height = int(height)

    upscaled = cropped.resize(size=(width, height))
    return upscaled




def ocr_tesseract(img: Image) -> str:
    return image_to_string(img)
