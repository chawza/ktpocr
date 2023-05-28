import os
import sys
from datetime import date

from unittest import TestCase

from dataclasses import dataclass
from typing import Dict, Union, List

from ktpocr import KTPExtractor, KTPIdentity

verbose = True if '-v' in sys.argv else False

ReportType = Dict[str, Union[float, bool]]

@dataclass
class TestResult:
    filepath: str
    accuracy: float
    result: dict
    identity: KTPIdentity

    def print_result(self):
        if verbose:
            self.draw_table()
        accuracy =f'{self.accuracy * 100:>17}%'
        print(f'{os.path.basename(self.filepath):20}: {accuracy:5}')
    
    def draw_table(self):
        print('\n',"="*50)

        for title, result in self.result.items():
            value = getattr(self.identity, title)
            if isinstance(value, date):
                value = str(value)
            print(f"{title:15}: {result * 100:>7.2f}%\t{value}")

class TestAccuracy(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.test_results: List[TestResult] = []

    def get_test_image_path(self, name: str) -> str:
        project_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(project_path, 'test', 'resources', name)

    def get_accuracy(self, report: ReportType) -> float:
        total_score = 0.0
        for _, value in report.items():
            if isinstance(value, float):
                total_score += value
            else:
                total_score += (1.0 if value == True else 0.0)
        avg = total_score/len(report.items())
        return avg

    def doCleanups(self) -> None:
        for result in self.test_results:
            result.print_result()


    def test_clean_image(self):
        ktp_truth = KTPIdentity(
            number="3171234567890123",
            name="MIRA SETIAWAN",
            birth_place="JAKARTA",
            birth_date=date(1986, 2, 18),
            sex="PEREMPUAN",
            full_address="JL. PASTI CEPAT A7/66",
            neigborhood="007/008",
            district="PEGADUNGAN",
            sub_district="KALIDERES BANGKAHULU",
            religion="ISLAM",
            marital="KAWIN",
            job="PEGAWAI SWASTA",
            nationality="WNI",
            valid_date=date(2017, 2, 22)
        )
        img_path = self.get_test_image_path('image_clean.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)

    def test_ktp1(self):
        ktp_truth = KTPIdentity(
            number="177104240190002",
            name="GALANG RAKE PRATAMA",
            birth_place="BENGKULU",
            birth_date=date(1993, 1, 4),
            sex="LAKI-LAKI",
            full_address="JLUNIB PERMA III NO 35 PERUMNAS UNIB",
            neigborhood="015 / 003",
            district="PEMATANG GUBERNUR",
            sub_district="MUARA BANGKAHULU",
            religion="ISLAM",
            marital="BELUM KAWIN",
            job="PELAJAR/MAHASISWA",
            nationality="WNI",
            valid_date=date(2017, 1, 24)
        )
        img_path = self.get_test_image_path('ktp1.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)

    def test_ktp2(self):
        ktp_truth = KTPIdentity(
            number="3217061804870007",
            name="ARIEF WIJAYA PUTRA",
            birth_place="BANDUNG",
            birth_date=date(1987, 4, 18),
            sex="LAKI-LAKI",
            full_address="JL. AMIR MAHMUD GG. SIRNAGALIH NO.62",
            neigborhood="005/006",
            district="CIBABAT",
            sub_district="CIMAHI UTARA",
            religion="ISLAM",
            marital="BELUM KAWIN",
            job="PELAJAR/MAHASISWA",
            nationality="WNI",
            valid_date="SEUMUR HIDUP"
        )
        img_path = self.get_test_image_path('ktp2.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)

    def test_ktp3(self):
        ktp_truth = KTPIdentity(
            number="3523160606800003",
            name="MAFTUCHIN",
            birth_place="TUBAN",
            birth_date=date(1980, 6, 6),
            sex="LAKI-LAKI",
            full_address="JL. AMIR MAHMUD GG. SIRNAGALIH NO.62",
            neigborhood="001/002",
            district="SUGIHARJO",
            sub_district="TUBAN",
            religion="ISLAM",
            marital="KAWIN",
            job="WIRASWASTA",
            nationality="WNI",
            valid_date=date(2017, 6, 6)
        )
        img_path = self.get_test_image_path('ktp3.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)

    def test_ktp5(self):
        ktp_truth = KTPIdentity(
            number="1204050503670001",
            name="EDO FURNAMA",
            birth_place="NIAS",
            birth_date=date(1967, 3, 5),
            sex="LAKI-LAKI",
            full_address="DUSUN II HILIHAMBAWA",
            neigborhood="001/003",
            district="HILIGODU TANASOE",
            sub_district="HILIDUHO",
            religion="KATHOLIK",
            marital="CERAI HIDUP",
            job="WARTAWAN",
            nationality="WNI",
            valid_date=date(2018, 3, 5)
        )
        img_path = self.get_test_image_path('ktp5.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)
    
    def test_ktp6(self):
        ktp_truth = KTPIdentity(
            number="3216061812590006",
            name="WIDIARSO",
            birth_place="PEMALANG",
            birth_date=date(1959, 12, 18),
            sex="LAKI-LAKI",
            full_address="SKU JL.SUMATRA BLOK B78/15",
            neigborhood="003/004",
            district="MEKARSARI",
            sub_district="TAMBUN SELATAN",
            religion="KATHOLIK",
            marital="KAWIN",
            job="KARYAWAN SWASTA",
            nationality="WNI",
            valid_date=date(2018, 12, 18)
        )
        img_path = self.get_test_image_path('ktp6.jpeg')

        extractor = KTPExtractor(img_path, treshold=150)
        identity = extractor.extract()
        
        result = identity.compare(ktp_truth)
        accuracy = self.get_accuracy(result)

        self.test_results.append(TestResult(img_path, accuracy, result, identity))
        self.assertGreaterEqual(accuracy, .8)