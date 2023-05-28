from PIL import Image, ImageFilter
from ktpocr.utils import KTPIdentity
from ktpocr.extractor import extract as extract_identity 
from ktpocr.ocr import ocr_tesseract, crop_text_area

class FailDetectText(Exception):
    pass

class KTPExtractor():
    def __init__(self, image, treshold = 150) -> None:
        self.img_path = image
        self.raw_image = Image.open(image)
        self.treshold = treshold

    def extract(self) -> KTPIdentity:
        self.gray_img = self.raw_image.convert('L')

        try:
            self.cropped_img = crop_text_area(self.gray_img)
        except ValueError:
            self.cropped_img = self.gray_img

        # self.processed_img = self.preprocess(self.cropped_img, treshold=self.treshold)
        self.ocr_result = ocr_tesseract(self.cropped_img)  # somehow unpreprocessed image is give btter result

        if self.ocr_result.strip() == '':
            raise FailDetectText()
            
        identity = extract_identity(self.ocr_result)
        return identity

    def preprocess(self, img: Image.Image, treshold = 150) -> Image.Image:
        # TODO: Current Preprocess doesn't give better result
        img = img.filter(ImageFilter.MedianFilter)
        img = img.point(lambda x: 255 if x > treshold else 0)
        return img
    
    def _save_all_image(self, path='./all_files.jpeg'):
        gray, cropped = self.gray_img, self.cropped_img,

        max_width = max(img.size[0] for img in [gray, cropped])
        total_height = sum(img.size[1] for img in [gray, cropped])

        canvas = Image.new('L', (max_width, total_height))

        offset = 0
        for img in [gray, cropped]:
            box = (0, offset)
            canvas.paste(img, box)
            offset += img.size[1]
        
        canvas.save(path)