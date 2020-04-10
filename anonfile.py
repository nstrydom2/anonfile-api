from pyapiwiz import Uri


class AnonFile(Uri):
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

    def list_servers(self):
        print(self.server_list.keys())
