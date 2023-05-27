from PIL import Image, ImageFilter

def preprocess(img: Image, treshold = 150) -> Image:
    img = img.convert("L")
    img = img.filter(ImageFilter.MedianFilter)
    img = img.point(lambda x: 255 if x > treshold else 0)

    return img