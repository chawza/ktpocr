from PIL import Image, ImageOps, ImageFilter
from dataclasses import dataclass
from datetime import date
from pytesseract import image_to_string
import re


@dataclass
class KTPIdentity:
    number: str
    name: str
    birth_place = str
    sex: str
    birth_date: date 
    full_address: str
    neigborhood: str
    district: str
    sub_district: str
    religion: str
    marital: str
    job: str
    nationality: str
    valid_date: date 



class KTPExtractor():
    def __init__(self, image) -> None:
        self.raw_image = Image.open(image)
        self.treshold = 150

    def preprocess(self):
        img = self.raw_image.convert("L")
        img = img.filter(ImageFilter.MedianFilter)
        img = img.point(lambda x: 255 if x > self.treshold else 0)
        return img
    
    def extract(self) -> KTPIdentity:
        ktp_img = self.preprocess()
        result = image_to_string(ktp_img)
        
        if not len(result):
            raise ValueError("No Data")

        result = self._clean_text(result)

        data = {
            number: str
            name: str
            birth_place = str
            sex: str
            birth_date: date 
            full_address: str
            neigborhood: str
            district: str
            sub_district: str
            religion: str
            marital: str
            job: str
            nationality: str
            valid_date: date 
        }
        for line in result.split("\n"):
            if "nik" in line.lower():
                try:
                    nik = line.split(':')[1]
                except KeyError:
                    nik = ""

                data.update({"number": nik})
        

        return KTPIdentity(**data)

    def _clean_text(self, text: str) -> str:
        text = text.strip()
        text = text.replace(r'\n+', '\n')
        print(text)
        return text
