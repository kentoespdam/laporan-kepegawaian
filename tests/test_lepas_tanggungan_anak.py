from unittest import TestCase

from icecream import ic

from app.models.lepas_tanggungan_anak import LepasTanggunganAnakModel, FilterLepasTanggunganAnak


class TestLepasTanggunganAnak(TestCase):
    def setUp(self):
        self.model = LepasTanggunganAnakModel()
        self.filter = FilterLepasTanggunganAnak.BULAN_INI

    def test_fetch(self):
        df = self.model.fetch(self.filter)
        self.assertEqual(df.empty, False)
        ic(df.to_dict("records"))

    def test_count(self):
        count=self.model.count(self.filter)
        ic(count)
        self.assertGreater(count, 0)
