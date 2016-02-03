import unittest
import tempfile
import pandas as pd
import requests
import httpretty
from stock_extractor.BarchartExtractor.sp_500_extract import SP500Extractor


class TestSP500Extractor(unittest.TestCase):
    def setUp(self):
        self.extractor = SP500Extractor()

    def test_get_sp500_full_data(self):
        self.extractor.get_sp500_full_data()
        self.assertTrue(self.extractor.df.shape[0] > 0)

