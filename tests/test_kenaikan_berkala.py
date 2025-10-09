from unittest import TestCase

from icecream import ic

from app.core.enums import FilterKenaikanBerkala, JenisSk
from app.models.kenaikan_berkala import KenaikanBerkalaModel
from app.services.kenaikan_berkala import KenaikanBerkalaService


class TestKenaikanBerkalaModel(TestCase):
    def setUp(self):
        self.kbm = KenaikanBerkalaModel()
        self.kbs = KenaikanBerkalaService()
        self.filter = FilterKenaikanBerkala.BULAN_INI
        self.jenis_sk = JenisSk.SK_KENAIKAN_GAJI_BERKALA

    def test_get_query(self):
        query = self.kbm._query_builder(self.kbm._base_query(), self.filter)
        where = self.kbm._condition_builder(self.kbm._base_condition(self.jenis_sk), self.filter)
        self.assertNotEqual(query, None)
        self.assertNotEqual(where, None)
        ic(query % where)

    def test_fetch(self):
        df = self.kbm.fetch(self.filter, self.jenis_sk)
        self.assertFalse(df.empty)
        filter = df["is_pending_gaji"].eq(True) | df["is_pending_pangkat"].eq(True)
        # ic(df[filter].to_dict("records"))
        ic(df.to_dict("records"))

    def test_fetch_service(self):
        df = self.kbs.fetch(self.filter, self.jenis_sk)
        self.assertFalse(df.empty)
        ic(df.to_dict("records"))
