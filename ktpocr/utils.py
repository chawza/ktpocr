from typing import Optional, Union
from dataclasses import dataclass, fields
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
    valid_date: Optional[Union[date, str]]

    @property
    def extracted_ration(self) -> float:
        total = 0
        count = 0

        for field in fields(self):
            if getattr(self, field.name) is not None:
                total += 1
            count += 1

        return total/count