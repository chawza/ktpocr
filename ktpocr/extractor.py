import re
from typing import List

from datetime import datetime

from ktpocr import KTPIdentity

DATE_FORMAT = "%d-%m-%Y"
RELGIION_LIST = ["ISLAM", "KATOLIK", "PROTESTAN", "HINDU", "BUDHA", "KONGHUCU"]


def match_patterns(input: str, patterns: List[str]):
    for pattern in patterns:
        cleaned = input.replace('( )*', '').upper().strip()
        if pattern in cleaned:
            return pattern
    return input


def search_nik(text: str) -> str | None:
    cleaned = re.sub(' *', '', text)
    search_nik = re.search("\d{16}", cleaned)
    if search_nik:
        return search_nik.group(0)
    else:
        return None
    

def extract(text: str) -> KTPIdentity:
    """
    @param text: A raw result of any OCR in a form of text 
    """
    # initate inital values
    identity = KTPIdentity(*[None for _ in range(14)])

    text = clean_text(text)

    for line in text.split("\n"):

        if (found_nik := search_nik(line)):
            if found_nik:
                identity.number = found_nik

        elif 'nama' in line.lower():
            name = re.sub("nama *:?", "", line, flags=re.IGNORECASE)
            name = name.replace(':', "").strip()
            identity.name = name

        elif 'tempat' in line.lower():
            dob = re.sub("tempat *:?", '', line, flags=re.IGNORECASE).strip()  # JAKARTA, 17-08-1945

            date_match = re.search("\d{2}-\d{2}-\d{4}", dob)  # 17-08-1945
            if date_match:
                match = date_match.group(0)
                identity.birth_date = datetime.strptime(match, DATE_FORMAT).date()

            if date_match:
                birth_place = re.sub(match, '', dob, flags=re.IGNORECASE)  # Jakarta, 
            else:
                birth_place = dob
            birth_place = birth_place.replace(',', '').strip()
            identity.birth_place = birth_place 

        elif 'alamat' in line.lower():
            address = re.sub('alamat', "", line, flags=re.IGNORECASE)
            identity.full_address = clean_field(address) 

        elif (rtrw_match := re.search('rt(.)*rw', line, flags=re.IGNORECASE)):
            neighborhood = line.replace(rtrw_match.group(0), '')
            identity.neigborhood = clean_field(neighborhood) 

        elif (district_match := re.search('kel(.)*desa', line, flags=re.IGNORECASE)):
            district = line.replace(district_match.group(0), '')
            identity.district = clean_field(district)

        elif (sub_district_match := re.search('kecamatan', line, flags=re.IGNORECASE)):
            sub_district = line.replace(sub_district_match.group(0), '')
            identity.sub_district = clean_field(sub_district)

        elif 'agama' in line.lower():
            religion = re.sub('agama', "", line, flags=re.IGNORECASE)
            religion = clean_field(religion)
            identity.religion = match_patterns(religion, RELGIION_LIST)

        elif 'perkawinan' in line.lower():
            marital = re.sub('(.)*perkawinan', "", line, flags=re.IGNORECASE)
            identity.marital = clean_field(marital)

        elif 'pekerjaan' in line.lower():
            job = re.sub('pekerjaan', "", line, flags=re.IGNORECASE)
            job = clean_field(job)
            identity.job = job

        elif 'negaraan' in line.lower():
            nationality = re.sub('(.)*negaraan', "", line, flags=re.IGNORECASE)
            identity.nationality = clean_field(nationality)

    return identity

def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub("(\n)+", "\n", text)
    return text

def clean_field(text: str) -> str:
    text = re.sub('-|:', '', text)
    text = text.strip()
    return text
