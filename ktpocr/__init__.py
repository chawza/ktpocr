from PIL import Image
from ktpocr.utils import KTPIdentity
from ktpocr.extractor import extract as extract_identity 
from ktpocr.image import preprocess
from ktpocr.ocr import ocr_tesseract

class KTPExtractor():
    def __init__(self, image, treshold = 150) -> None:
        self.img_path = image
        self.raw_image = Image.open(image)
        self.treshold = treshold

    def extract(self) -> KTPIdentity:
        self.processed_img = preprocess(self.raw_image, treshold=self.treshold)
        ocr_result = ocr_tesseract(self.processed_img)
        identity = extract_identity(ocr_result)
        return identity
