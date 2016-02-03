import unittest
import tempfile
import pandas as pd
import requests
import httpretty
from stock_extractor.BaseExtractor.BaseExtractor import BaseExtractor


class TestBaseExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = BaseExtractor()

    @httpretty.activate
    def test_get_url_response(self):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, "http://base_test.com",
                               body='mock response')
        url = r'http://base_test.com'
        resp = self.extractor._get_url_response(url, {'a': 'b'})
        self.assertEqual(resp.text, 'mock response')
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {'a': ['b']})

    def test_get_dataframe(self):
        self.assertEqual(self.extractor.df, None)

    def test_save_to_csv(self):
        tmp_csv = tempfile.NamedTemporaryFile(suffix='.csv')
        self.extractor.df = pd.DataFrame([[1, 2], [3, 4]])
        self.extractor.save_to_csv(tmp_csv.name)
        with open(tmp_csv.name) as f:
            self.assertTrue('1' in f.readlines()[1])
