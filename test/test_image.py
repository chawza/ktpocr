from unittest import TestCase
from ktpocr.extractor import KTPExtractor
import os
from datetime import date 

class Test(TestCase):
    project_path = os.path.dirname(os.path.dirname(__file__)) 
    clean_image_path = os.path.join(
        project_path,
        "test/resources/image_clean.jpeg"
    )

    def test_clean_image(self):
        extractor = KTPExtractor(self.clean_image_path)
        identity = extractor.extract()

        self.assertEqual(identity.number, "3171234567890123")
        self.assertEqual(identity.name, "MIRA SETIAWAN")
        self.assertEqual(identity.birth_place, "JAKARTA")
        self.assertEqual(identity.birth_date, date(1986, 2, 18)) 
        self.assertTrue("JL. PASTI CEPAT A7/66" in identity.full_address,)
        self.assertEqual(identity.neigborhood, "007/008")
        self.assertEqual(identity.district, "PEGADUNGAN")
        self.assertEqual(identity.sub_district, "KALIDERES")
        # self.assertEqual(identity.religion, "ISLAM")
        self.assertEqual(identity.marital, "KAWIN")
        self.assertEqual(identity.job, "PEGAWAI SWASTA")
        self.assertTrue("WNI", identity.nationality)