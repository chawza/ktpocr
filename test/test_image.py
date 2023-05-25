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

        self.assertTrue("3171234567890123" in identity.number)
        self.assertTrue("MIRA SETIAWAN" in identity.name)
        self.assertTrue("JAKARTA" in identity.birth_place)
        self.assertEqual(identity.birth_date, date(1986, 2, 18)) 
        self.assertTrue("JL. PASTI CEPAT A7/66" in identity.full_address,)
        self.assertTrue("007/008" in identity.neigborhood)
        self.assertTrue("PEGADUNGAN" in identity.district)
        self.assertTrue("KALIDERES" in identity.sub_district)
        self.assertTrue("ISLAM" in identity.religion)
        self.assertTrue("KAWIN" in identity.marital)
        self.assertTrue("PEGAWAI SWASTA" in identity.job)
        self.assertTrue("WNI", identity.nationality)