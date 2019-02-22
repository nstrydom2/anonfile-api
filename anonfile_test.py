import unittest
import anonfile

class AnonfileTest(unittest.TestCase):
    # Instantiate the test object
    def setUp(self):
        self.test_obj = anonfile.AnonFile()

    def test_returns_success_on_upload_file(self):
        status, file_obj = self.test_obj.upload_file('/home/ghost/my_test01.zip')

        assert (status is True)
        assert (file_obj is not None)
