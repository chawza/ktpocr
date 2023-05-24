from unittest import TestCase
from ktpocr.extractor import KTPExtractor
import os
from datetime import date 

class Test(TestCase):
    project_path = os.path.dirname(os.path.dirname(__file__)) 
    img_path = os.path.join(
        project_path,
        "test/resources/image_clean.jpeg"
    )

    def test_test(self):
        extractor = KTPExtractor(self.img_path)
        # img = extractor.preprocess()
        # img.save(os.path.join(self.project_path, 'test/resources/output1.jpg'))
        identity = extractor.extract()

        self.assertTrue(identity.name, "MIRA SETIAWAN")
        self.assertTrue(identity.birth_place, "JAKARTA")
        self.assertTrue(identity.birth_date, date(1986, 2, 18)) 
        self.assertAlmostEqual(identity.full_address, "JL. PASTI CEPAT A7/66")
        self.assertTrue(identity.neigborhood, "007/008")
        self.assertTrue(identity.district, "PEGADUNGAN")
        self.assertTrue(identity.sub_district, "KALIDERES")
        self.assertTrue(identity.religion, "ISLAM")
        self.assertTrue(identity.marital, "KAWIN")
        self.assertTrue(identity.job, "PEGAWAI SWASTA")
        self.assertTrue(identity.nationality, "WNI")