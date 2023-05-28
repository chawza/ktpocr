from typing import Optional, Union
from dataclasses import dataclass, fields
from datetime import date
from difflib import SequenceMatcher

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
    def extracted_ratio(self) -> float:
        total = 0
        count = 0

        for field in fields(self):
            if getattr(self, field.name) is not None:
                total += 1
            count += 1

        return total/count
    
    def compare(self, truth: 'KTPIdentity') -> dict:
        char_fields = [field.name for field in fields(truth) if field.type == Optional[str]]
        date_fields = [field.name for field in fields(truth) if field.type == Optional[date]]

        report = {}

        for field in char_fields:
            if getattr(self, field):
                value = SequenceMatcher(
                    None,
                    getattr(truth, field),
                    getattr(self, field)
                ).ratio()
            else:
                value = 0

            report.update({ field: value })

        for field in date_fields:
            if getattr(self, field):
                value = getattr(truth, field) == getattr(self, field)
            else:
                value = False

            report.update({ field: value })

        return report