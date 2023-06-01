#!/usr/bin/env python3

import hashlib
import unittest
from pathlib import Path
from unittest.mock import patch

from faker import Faker

from src.anonfile import AnonFile
from mock import MockData

TOKEN = None


def test_option(token):
    global TOKEN
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


class TestAnonFile(unittest.TestCase):
    """Test cases for the AnonFile class."""

    @classmethod
    def setUpClass(cls):
        cls.anon = init_anon()
        cls.test_file = Path("tests/original_topsecret.mp4")
        cls.test_small_file = "https://anonfiles.com/93k5x1ucu0/test_txt"
        cls.test_med_file = "https://anonfiles.com/P0mev3tfz7/topsecret_mp4"
        cls.garbage = []

    @patch('anonfile.requests.Session.post')
    def test_upload(self, mocked_session_post):
        """ Tests a mocked upload """

        # Arrange
        raw_response = {
            'data': {
                'file': {
                    'url': {
                        'full': 'https://anonfiles.com/A66bG9t0z1/topsecret_mp4',
                        'short': 'https://anonfiles.com/A66bG9t0z1'
                    },
                    'metadata': {
                        'id': 'A66bG9t0z1',
                        'size': {
                            'readable': '3.37 MB',
                            'bytes': 3537832
                        },
                        'name': 'topsecret.mp4'
                    }
                }
            },
            'status': True
        }
        json_response = MockData.get_json_response(raw_response)

        mocked_session_post.side_effect = [json_response]

        # Act
        upload = self.anon.upload(self.test_file, progressbar=True, enable_logging=True)

        # Assert
        self.assertTrue(upload.status, msg="Expected 200 HTTP Error Code")
        self.assertTrue(all([upload.url.scheme, upload.url.netloc, upload.url.path]), msg="Invalid URL.")

    @patch('anonfile.requests.Session.get')
    def test_preview(self, mocked_session_get):
        """ Tests mocked preview API request """

        # Arrange
        raw_response = {
            'status': True,
            'data': {
                'file': {
                    'url': {
                        'short': 'https://anonfiles.com/P0mev3tfz7',
                        'full': 'https://anonfiles.com/P0mev3tfz7/topsecret_mp4'
                    },
                    'metadata': {
                        'size': {
                            'bytes': 3537832,
                            'readable': '3.37 MB'
                        },
                        'name': 'topsecret_mp4',
                        'id': 'P0mev3tfz7'
                    }
                }
            }
        }
        json_response = MockData.get_json_response(raw_response)
        html_response = MockData.get_html_response("tests/preview.html")

        mocked_session_get.side_effect = [json_response, html_response]

        # Act
        preview = self.anon.preview(self.test_med_file)

        # Assert
        self.assertTrue(preview.status, msg="Error in status property.")
        self.assertEqual(self.test_med_file, preview.url.geturl(), msg="Error in URL property.")
        self.assertEqual("P0mev3tfz7", preview.id, msg="Error in ID property.")
        self.assertEqual("topsecret.mp4", preview.file_path.name, msg="Error in name property.")
        self.assertEqual(3537832, preview.size, msg="Error in size property.")

    @patch('anonfile.requests.Session.get')
    def test_download(self, mocked_session_get):
        """ Tests mocked file download with a simulated stream """

        # Arrange
        raw_response = {
            'status': True,
            'data': {
                'file': {
                    'url': {
                        'short': 'https://anonfiles.com/P0mev3tfz7',
                        'full': 'https://anonfiles.com/P0mev3tfz7/topsecret_mp4'
                    },
                    'metadata': {
                        'size': {
                            'bytes': 3537832,
                            'readable': '3.37 MB'
                        },
                        'name': 'topsecret_mp4',
                        'id': 'P0mev3tfz7'
                    }
                }
            }
        }
        json_response = MockData.get_json_response(raw_response)
        html_response = MockData.get_html_response("tests/preview.html")
        file_response = MockData.get_file_response("tests/original_topsecret.mp4")

        mocked_session_get.side_effect = [json_response, html_response, file_response]

        # Act
        download = self.anon.download(self.test_med_file, progressbar=True, enable_logging=True)

        # Assert
        self.assertTrue(download.file_path.exists(), msg="Download not successful.")
        self.assertEqual(download.file_path.name, "topsecret.mp4", msg="Different file in download path detected.")
        self.garbage.append(download.file_path)

    @patch('anonfile.requests.Session.get')
    def test_multipart_encoded_files(self, mocked_session_get):
        """ Tests download data integrity utilizing mocked file download """

        # Arrange
        raw_response = {
            'status': True,
            'data': {
                'file': {
                    'url': {
                        'short': 'https://anonfiles.com/P0mev3tfz7',
                        'full': 'https://anonfiles.com/P0mev3tfz7/topsecret_mp4'
                    },
                    'metadata': {
                        'size': {
                            'bytes': 3537832,
                            'readable': '3.37 MB'
                        },
                        'name': 'topsecret_mp4',
                        'id': 'P0mev3tfz7'
                    }
                }
            }
        }
        json_response = MockData.get_json_response(raw_response)
        html_response = MockData.get_html_response("tests/preview.html")
        file_response = MockData.get_file_response("tests/original_topsecret.mp4")

        mocked_session_get.side_effect = [json_response, html_response, file_response]

        # Act
        download = self.anon.download(self.test_med_file, progressbar=True, enable_logging=True)

        # Assert
        self.assertEqual("d41d8cd98f00b204e9800998ecf8427e", md5_checksum(download.file_path), msg="MD5 hash is corrupted.")
        self.garbage.append(download.file_path)

    @classmethod
    def tearDownClass(cls):
        for file in cls.garbage:
            remove_file(file)
