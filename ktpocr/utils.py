from typing import Optional
from dataclasses import dataclass
from datetime import date

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
