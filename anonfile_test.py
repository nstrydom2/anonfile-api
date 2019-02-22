import unittest
import anonfile
import json

class AnonfileTest(unittest.TestCase):
    # Instantiate the test object
    def setUp(self):
        self.my_api_key = ''

        self.test_obj = anonfile.AnonFile(self.my_api_key)

    def test_returns_success_on_upload_file(self):
        status, file_obj = self.test_obj.upload_file('/home/ghost/my_test01.zip')

        print("[*] File object -- " + json.dumps(file_obj))

        assert (status is True)
        assert (file_obj is not None)
