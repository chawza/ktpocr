import os
import sys
from datetime import date

from unittest import TestCase
from difflib import SequenceMatcher

from dataclasses import fields
from typing import Any, Optional, Dict, Union

from ktpocr import KTPExtractor, KTPIdentity

verbose = True if '-v' in sys.argv else False

ReportType = Dict[str, Union[float, bool]]

class TestAccuracy(TestCase):

    def get_test_image_path(self, name: str) -> str:
        project_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(project_path, 'test', 'resources', name)

    def validate_identity(self, truth: KTPIdentity, target: KTPIdentity):
        # self.assertTrue(truth.number in target.number)
        # self.assertTrue(truth.name in target.name)
        # self.assertTrue(truth.birth_place in target.birth_place)
        # self.assertEqual(truth.birth_date, target.birth_date)
        # self.assertTrue(truth.full_address in target.full_address)
        # self.assertTrue(truth.neigborhood in target.neigborhood)
        # self.assertTrue(truth.district in target.district)
        # self.assertTrue(truth.sub_district in target.sub_district)
        # self.assertTrue(truth.religion in target.religion)
        # self.assertTrue(truth.marital in target.marital)
        # self.assertTrue(truth.job in target.job)
        # self.assertTrue(truth.nationality in target.nationality)
        char_fields = [field.name for field in fields(truth) if field.type == Optional[str]]
        date_fields = [field.name for field in fields(truth) if field.type == Optional[date]]

        report = {}

        for field in char_fields:
            if getattr(target, field):
                value = SequenceMatcher(
                    None,
                    getattr(truth, field),
                    getattr(target, field)
                ).ratio()
            else:
                value = 0

            report.update({ field: value })

        for field in date_fields:
            if getattr(target, field):
                value = getattr(truth, field) == getattr(target, field)
            else:
                value = False

            report.update({ field: value })

        if verbose:
            self.draw_table(report, truth, target)
        accuracy = self.get_accuracy(report)
        return accuracy
        

    def draw_table(self, report: ReportType, truth: KTPIdentity, target: KTPIdentity):
        print('\n',"="*50)

        for title, result in report.items():
            truth_value = getattr(truth, title)
            target_value = getattr(target, title)

            if isinstance(result, bool):
                result = 1.0 if result == True else 0.0

            print(f"{title:15}: {result * 100:>7.2f}%\t{str(truth_value):30}\t{str(target_value):30}")


    def get_accuracy(self, report: ReportType) -> float:
        total_score = 0.0
        for _, value in report.items():
            if isinstance(value, float):
                total_score += value
            else:
                total_score += (1.0 if value == True else 0.0)
        avg = total_score/len(report.items())
        if verbose:
            print(f"{'AVG':15}: {avg * 100:>7.2f}%")

        return avg
        


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
        extractor = KTPExtractor(img_path)
        identity = extractor.extract()
        extractor.processed_img.save(self.get_test_image_path('processed_clean_ktp.jpeg'))
        accuracy = self.validate_identity(ktp_truth, identity)
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
        extractor = KTPExtractor(img_path, save_processed=True)
        identity = extractor.extract()
        accuracy = self.validate_identity(ktp_truth, identity)
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
        extractor = KTPExtractor(img_path, treshold=130)
        identity = extractor.extract()
        accuracy = self.validate_identity(ktp_truth, identity)
        extractor.processed_img.save(self.get_test_image_path('processed_ktp2.jpeg'))
        self.assertGreaterEqual(accuracy, .8)