#!/usr/bin/env python3

import hashlib
import json
import random
import subprocess
import unittest
from pathlib import Path
from unittest import skip
from unittest.mock import patch, Mock, MagicMock

from faker import Faker
from requests import Response

from src.anonfile import AnonFile, get_logfile_path

TOKEN = None


def test_option(token):
    TOKEN = token


def md5_checksum(path: Path) -> str:
    with open(path, mode='rb') as file_handler:
        return hashlib.md5(file_handler.read()).hexdigest()


def init_anon() -> AnonFile:
    chrome_ua = Faker().chrome(version_from=90, version_to=93, build_from=4400, build_to=4500)
    return AnonFile(token=TOKEN, user_agent=chrome_ua) if TOKEN else AnonFile(user_agent=chrome_ua)


def write_file(file: str, lines: list) -> Path:
    with open(file, mode='w+') as file_handler:
        file_handler.write('\n'.join(lines))
        return Path(file)


def remove_file(file: str) -> None:
    Path(file).unlink() if Path(file).exists() else None


class TestAnonFileLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anon = init_anon()
        cls.test_file = Path("tests/topsecret.mp4")
        cls.test_small_file = "https://anonfiles.com/93k5x1ucu0/test_txt"
        cls.test_med_file = "https://anonfiles.com/P0mev3tfz7/topsecret_mp4"
        cls.garbage = []

    def test_upload(self):
        upload = self.anon.upload(self.test_file, progressbar=True, enable_logging=True)
        self.assertTrue(upload.status, msg="Expected 200 HTTP Error Code")
        self.assertTrue(all([upload.url.scheme, upload.url.netloc, upload.url.path]), msg="Invalid URL.")

    @patch('anonfile.requests.Session.get')
    def test_preview(self, mocked_session_get):
        json_content = open('./preview.json', encoding='utf-8').read()
        html_content = open('./preview.html', 'r', encoding='utf-8').read()

        json_response = Mock(spec=Response)
        json_response.__enter__ = MagicMock(return_value=json_response)
        json_response.__exit__ = MagicMock()
        json_response.status_code = 200
        json_response.json.return_value = json.loads(json_content)

        html_response = Mock(spec=Response)
        html_response.__enter__ = MagicMock(return_value=html_response)
        html_response.__exit__ = MagicMock()
        html_response.status_code = 200
        html_response.text = html_content

        mocked_session_get.side_effect = [json_response, html_response]

        preview = self.anon.preview(self.test_med_file)
        self.assertTrue(preview.status, msg="Error in status property.")
        self.assertEqual(self.test_med_file, preview.url.geturl(), msg="Error in URL property.")
        self.assertEqual("P0mev3tfz7", preview.id, msg="Error in ID property.")
        self.assertEqual("original_topsecret.mp4", preview.file_path.name, msg="Error in name property.")
        self.assertEqual(3537832, preview.size, msg="Error in size property.")

    @patch('anonfile.requests.Session.get')
    def test_download(self, mocked_session_get):
        json_content = open('./preview.json', encoding='utf-8').read()
        html_content = open('./preview.html', 'r', encoding='utf-8').read()

        json_response = Mock(spec=Response)
        json_response.__enter__ = MagicMock(return_value=json_response)
        json_response.__exit__ = MagicMock()
        json_response.status_code = 200
        json_response.json.return_value = json.loads(json_content)

        html_response = Mock(spec=Response)
        html_response.__enter__ = MagicMock(return_value=html_response)
        html_response.__exit__ = MagicMock()
        html_response.status_code = 200
        html_response.text = html_content

        download_bytes = open('./original_topsecret.mp4', 'rb').read()

        # Create a generator to mimic streamed content
        response_data = (chunk for chunk in download_bytes)

        # Mock the Response object's `iter_content` method to return the generator
        download_response = Mock(spec=Response)
        download_response.__enter__ = MagicMock(return_value=download_response)
        download_response.__exit__ = MagicMock()
        download_response.iter_content.return_value = response_data

        mocked_session_get.side_effect = [json_response, html_response, download_response]

        download = self.anon.download(self.test_med_file, progressbar=True, enable_logging=True)
        self.assertTrue(download.file_path.exists(), msg="Download not successful.")
        self.assertEqual(download.file_path.name, self.test_file.name, msg="Different file in download path detected.")
        self.garbage.append(download.file_path)

    def test_multipart_encoded_files(self):
        # use pre-computed checksum for faster unit tests
        download = self.anon.download(self.test_med_file, progressbar=True, enable_logging=True)
        self.assertEqual("4578bdb7cc943f2280d567479794bc81", md5_checksum(download.file_path), msg="MD5 hash is corrupted.")
        self.garbage.append(download.file_path)

    @classmethod
    def tearDownClass(cls):
        for file in cls.garbage:
            remove_file(file)


class TestAnonFileCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anon = init_anon()
        cls.test_urls = [
            "https://anonfiles.com/n5j2O8G9u0/test_txt",
            "https://anonfiles.com/pdj2O8Gbud/test_txt",
            "https://anonfiles.com/n5j2O8G9u0/test_txt"
        ]
        cls.test_url = random.choice(cls.test_urls)
        cls.batch_file = write_file('batch.txt', cls.test_urls)
        cls.logfile = get_logfile_path()

    def test_cli_download(self):
        call = subprocess.call("anonfile --verbose download --url %s --no-check" % self.test_url, shell=True)
        self.assertFalse(call, msg=f"Download failed for: {self.test_url!r}")

    def test_cli_batch_download(self):
        call = subprocess.call("anonfile --verbose --logging download --batch-file %s --no-check" % self.batch_file, shell=True)
        self.assertFalse(call, msg=f"Download failed for: {str(self.batch_file)!r}")

    def test_cli_log(self):
        print()
        call = subprocess.call("anonfile log --read", shell=True)
        self.assertTrue(self.logfile.exists() and (call == 0), msg=f"Error: no log file produced in {str(self.logfile)!r}")

    @classmethod
    def tearDownClass(cls):
        remove_file(cls.batch_file)
        remove_file(cls.logfile)
