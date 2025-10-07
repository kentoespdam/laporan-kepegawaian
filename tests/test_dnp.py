from unittest import TestCase

from icecream import ic

from core.model.dnp import fetch_dnp
from core.model.duk import fetch_duk
from core.services.dnp import fetch_dnp_data


class Test(TestCase):
    def test_fetch_dnp(self):
        df=fetch_dnp()
        self.assertFalse(df.empty)
        ic(df.head().to_dict("records"))

    def test_fetch_dnp_service(self):
        data=fetch_dnp_data()
        self.assertFalse(data["dnp"].empty)
        self.assertFalse(data["organisasi"].empty)
        ic(data["dnp"].head().to_dict("records"))
        ic(data["organisasi"].head().to_dict("records"))