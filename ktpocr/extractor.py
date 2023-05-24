from PIL import Image, ImageFilter
from dataclasses import dataclass
from datetime import date, datetime
from pytesseract import image_to_string
import re
from typing import Optional
from string import ascii_letters


DATE_FORMAT = "%d-%m-%Y"


@dataclass
class KTPIdentity:
    number: Optional[str]
    name: Optional[str]
    birth_place: Optional[str]
    sex: Optional[str]
    birth_date: Optional[date] 
    full_address: Optional[str]
    neigborhood: Optional[str]
    district: Optional[str]
    sub_district: Optional[str]
    religion: Optional[str]
    marital: Optional[str]
    job: Optional[str]
    nationality: Optional[str]
    valid_date: Optional[date] 


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

        result = self._clean_result(result)

        # initate inital values
        identity = KTPIdentity(*[None for _ in range(14)])

        for line in result.split("\n"):
            if "nik" in line.lower():
                nik_match = re.search("\d{16}", line)
                if nik_match:
                    nik = nik_match.group(0)
                    identity.number = self._clean_field(nik)

            elif 'nama' in line.lower():
                name = re.sub("nama", "", line, flags=re.IGNORECASE)
                name = name.replace(':', "").strip()
                identity.name = name

            elif 'tempat' in line.lower():
                try:
                    field = line.split(":")[1]
                    place = [char for char in field if char in ascii_letters]
                    date_match= re.search("\d{2}-\d{2}-\d{4}", field)
                    if date_match:
                        match = date_match.group(0)
                        identity.birth_date = datetime.strptime(match, DATE_FORMAT).date()
                    identity.birth_place = ''.join(place)
                except KeyError:
                    pass
            
            elif 'alamat' in line.lower():
                address = re.sub('alamat', "", line, flags=re.IGNORECASE)
                identity.full_address = self._clean_field(address) 

            elif (rtrw_match := re.search('rt(.)*rw', line, flags=re.IGNORECASE)):
                neighborhood = line.replace(rtrw_match.group(0), '')
                identity.neigborhood = self._clean_field(neighborhood) 

            elif (district_match := re.search('kel(.)*desa', line, flags=re.IGNORECASE)):
                district = line.replace(district_match.group(0), '')
                identity.district = self._clean_field(district)

            elif (sub_district_match := re.search('kecamatan', line, flags=re.IGNORECASE)):
                sub_district = line.replace(sub_district_match.group(0), '')
                identity.sub_district = self._clean_field(sub_district) 

            elif 'agama' in line.lower():
                religion = re.sub('agama', "", line, flags=re.IGNORECASE)
                identity.religion = self._clean_field(religion) 

            elif 'perkawinan' in line.lower():
                marital = re.sub('(.)*perkawinan', "", line, flags=re.IGNORECASE)
                identity.marital = self._clean_field(marital)

            elif 'pekerjaan' in line.lower():
                job = re.sub('pekerjaan', "", line, flags=re.IGNORECASE)
                job = self._clean_field(job)
                identity.job = job

            elif 'negaraan' in line.lower():
                nationality = re.sub('(.)*negaraan', "", line, flags=re.IGNORECASE)
                identity.nationality = self._clean_field(nationality) 

        return identity

    def _clean_result(self, text: str) -> str:
        text = text.strip()
        text = re.sub("(\n)+", "\n", text)
        return text
    
    def _clean_field(self, text: str) -> str:
        text = re.sub('-|:', '', text)
        text = text.strip()
        return text
