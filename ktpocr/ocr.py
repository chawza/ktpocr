from pytesseract import image_to_string, image_to_boxes, Output, image_to_data
from PIL.Image import Image

def get_text_area(img: Image) -> Image:
    # result = image_to_boxes(img, output_type=Output.DICT)

    # left = min(result['left'])
    # top = max(result['top']) 
    # right = max(result['right']) 
    # bottom = max(result['bottom']) 

    left = 9999 
    top = 9999 
    right = 0 
    bottom = 0 

    result = image_to_data(img, output_type=Output.STRING)
    words = result.split('\n')[1:]
    words = [word.split('\n') for word in words if word != '']

    lefts = [int(word[5]) for word in words]
    tops = [int(word[6]) for word in words]
    widths = [int(word[7]) for word in words]
    heights = [int(word[8]) for word in words]

    for row in result.split('\n')[1:]:
        word = row.split('\t')
        if row == '':
            continue
        wleft = int(word[5])
        wtop = int(word[6])
        wwidth = int(word[7])
        wheight = int(word[8])

        left = min(left, wleft)
        top = min(top, wtop)

        wright = wleft + wwidth
        right = max(right, wright)

        wbottom = wtop + wheight
        bottom = max(bottom, wbottom)

    # left, upper, right, lower
    coordinte = (left, top, right, bottom)
    print(coordinte)
    # print(result)
    return img.crop(coordinte)




def ocr_tesseract(img: Image) -> str:
    return image_to_string(img)
