import requests
import net
import json

from bs4 import BeautifulSoup

class AnonFile():
    def __init__(self, api_key):
        # Api endpoint
        self.anonfile_endpoint_url = 'https://anonfile.com/api/'

        # User specific api key
        self.api_key = api_key

        # Set timeout (connect, read)
        self.timeout = (5, 5)

    # Custom timemout constructor
    def __init__(self, api_key , custom_timeout):
        # Api endpoint
        self.anonfile_endpoint_url = 'https://anonfile.com/api/'

        # User specific api key
        self.api_key = api_key

        # Set timeout (connect, read)
        self.timeout = custom_timeout

    # Takes file path and uploads file returning the url
    # to download file after the upload is complete, elses
    # return None if exception is thrown
    def upload_file(self, file_path):
        service = 'upload'

        try:
            file_upload = {'file': open(file_path, 'rb')}
            response = requests.post(self.anonfile_endpoint_url + service + self.api_key,
                                     files=file_upload, verify=True)

            return response.json()['status'], response.json()['data']['file']['url']['full']

        except Exception as ex:
            print("[*] Error -- " + str(ex))

            return None

    # Automatically downloads from anonfile.com based
    # on the given url
    def download_file(self, url):
        try:
            reponse = requests.get(url, timeout=self.timeout)
            soup = BeautifulSoup(reponse.text, 'lxml')
            download_url = soup.find_all('a')[0].attrs['href']

            # download code goes here

        except Exception as ex:
            print("[*] Error -- " + str(ex))
 
