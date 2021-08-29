#!/usr/bin/env python3

import hashlib
import unittest
from pathlib import Path

from src.anonfile import AnonFile

TOKEN = None

def test_option(token):
    TOKEN = token

def md5_checksum(path: Path) -> str:
    with open(path, mode='rb') as file_handler:
        return hashlib.md5(file_handler.read()).hexdigest()

class TestAnonFile(unittest.TestCase):
    def setUp(self):
        self.anon = AnonFile(TOKEN) if TOKEN else AnonFile()
        self.test_file = Path("tests/test.txt")
        self.test_small_file = "https://anonfiles.com/93k5x1ucu0/test_txt"
        self.test_med_file = "https://anonfiles.com/b7NaVd0cu3/topsecret_mkv"

    def test_upload(self):
        upload = self.anon.upload(self.test_file, progressbar=True, enable_logging=True)
        self.assertTrue(upload.status, msg="Expected 200 HTTP Error Code")
        self.assertTrue(all([upload.url.scheme, upload.url.netloc, upload.url.path]), msg="Invalid URL.")

    def test_preview(self):
        preview = self.anon.preview(self.test_small_file)
        self.assertTrue(preview.status, msg="Error in status property.")
        self.assertEqual(self.test_small_file, preview.url.geturl(), msg="Error in URL property.")
        self.assertEqual("93k5x1ucu0", preview.id, msg="Error in ID property.")
        self.assertEqual("test.txt", preview.file_path.name, msg="Error in name property.")
        self.assertEqual(271, preview.size, msg="Error in size property.")

    def test_download(self):
        download = self.anon.download(self.test_small_file, progressbar=True, enable_logging=True)
        self.assertTrue(download.file_path.exists(), msg="Download not successful.")
        self.assertEqual(download.file_path.name, self.test_file.name, msg="Different file in download path detected.")
        download.file_path.unlink()

    def test_multipart_encoded_files(self):
        # use pre-computed checksum for faster unit tests
        download = self.anon.download(self.test_med_file, progressbar=True, enable_logging=True)
        self.assertEqual("06b6a6bea6ba82900d144d3b38c65347", md5_checksum(download.file_path), msg="MD5 hash is corrupted.")
        download.file_path.unlink()
