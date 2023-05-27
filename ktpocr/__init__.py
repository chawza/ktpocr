from PIL import Image
from ktpocr.utils import KTPIdentity
from ktpocr.extractor import extract as extract_identity 
from ktpocr.image import preprocess
from ktpocr.ocr import ocr_tesseract

class KTPExtractor():
    def __init__(self, image, save_processed=False) -> None:
        self.img_path = image
        self.raw_image = Image.open(image)
        self.treshold = 150
        self.save_processed = save_processed

    def extract(self) -> KTPIdentity:
        ktp_img = preprocess(self.raw_image)
        ocr_result = ocr_tesseract(ktp_img)
        identity = extract_identity(ocr_result)
        return identity
