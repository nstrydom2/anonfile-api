import wget
import requests

from bs4 import BeautifulSoup
from functools import wraps


class AnonFile():
    # Custom timeout needs to be a tuple (connection_timeout, read_timeout)
    def __init__(self, api_key=None, server=None, uri=None, custom_timeout=None):
        # openload.cc letsupload.cc megaupload.nz bayfiles.com
        self.server_list = {'anonfile': 'https://anonfile.com',
                        'openload': 'https://openload.cc',
                       'letsupload': 'https://letsupload.cc',
                       'megaupload': 'https://megaupload.nz',
                       'bayfiles': 'https://bayfiles.com'}

        # Api endpoint
        if server not in self.server_list:
            if uri is not None:
                self.anonfile_endpoint_url = uri
            else:
                self.anonfile_endpoint_url = 'https://anonfile.com/api'
        else:
            self.anonfile_endpoint_url = self.server_list[server] + '/api'

        # User specific api key
        self.api_key = '?token=' + api_key

        # Dev can set their own custom timeout as
        # to accommodate slower internet connections
        if custom_timeout is not None:
            self.timeout = custom_timeout
        else:
            # Set timeout (connect, read)
            self.timeout = (5, 5)

    def authenticated(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                if self.api_key is not None:
                    return func(self, *args, **kwargs)
                else:
                    raise Exception("Api key is none, please obtain an Api key.")
            except Exception as ex:
                print("[!] Error -- " + str(ex))
        return wrapper

    def list_servers(self):
        print(self.server_list.keys())

    # Takes file path and uploads file returning the url
    # to download file after the upload is complete, else
    # return None if exception is thrown
    @authenticated
    def upload_file(self, file_path):
        # Service endpoint name
        service = '/upload'

        # Return variables
        status = False

        try:
            file_upload = {'file': open(file_path, 'rb')}

            # Post method, upload file and receive callback
            response = requests.post(self.anonfile_endpoint_url + service + self.api_key,
                                     files=file_upload, verify=True, timeout=self.timeout)

            status = bool(response.json()['status'])

            # File info, file json object as stated at https://anonfile.com/docs/api
            file_obj = response.json()['data']['file']

            if not status:
                raise Exception("File upload was not successful.")

            return status, file_obj

        except Exception as ex:
            print("[*] Error -- " + str(ex))

            return status, None

    # Automatically downloads from anonfile.com based
    # on the given url in file_obj. A json object containing
    # meta data about the uploaded file
    @authenticated
    def download_file(self, file_obj, location=None):
        # Scrapes the provided url for the url to the
        # actual file. Only called by 'download_file()'
        def scrape_file_location(url):
            # Get method, retrieving the web page
            response = requests.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'lxml')

            return soup.find_all('a')[1].attrs['href']

        try:
            download_url = scrape_file_location(file_obj['url']['full'])

            print(download_url)

            # download code goes here
            if download_url is not None:
                wget.download(download_url, location)

        except Exception as ex:
            print("[*] Error -- " + str(ex))
