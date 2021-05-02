#!/usr/bin/env python3

import unittest
from pathlib import Path

from src.anonfile import AnonFile

def test_option(token):
    global TOKEN
    TOKEN = token


class TestAnonFile(unittest.TestCase):
    def setUp(self):
        self.anon = AnonFile(TOKEN)
        self.test_file = Path("tests/test.txt")
        self.test_path = "https://anonfiles.com/9ee1jcu6u9/test_txt"

    def test_upload(self):
        result = self.anon.upload(self.test_file)
        self.assertTrue(result.status, msg="Expected 200 HTTP Error Code")
        self.assertTrue(all([result.url.scheme, result.url.netloc, result.url.path]), msg="Invalid URL.")

    def test_download(self):
        result = self.anon.download(self.test_path)
        self.assertTrue(result.exists(), msg="Download not successful.")
        self.assertEqual(result.name, self.test_file.name, msg="Different file in download path detected.")
        result.unlink(missing_ok=True)        
