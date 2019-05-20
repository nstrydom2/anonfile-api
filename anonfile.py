from pyapiwiz import Uri

class AnonFile(Uri):
    # Custom timeout needs to be a tuple (connection_timeout, read_timeout)
    def __init__(self, api_key, server=None, uri=None, custom_timeout=None):
        server_list = {}

        # Api endpoint
        if server not in server_list:
            if uri is not None:
                self.anonfile_endpoint_url = uri
            else:
                self.anonfile_endpoint_url = 'https://anonfile.com/api'
        else:
            self.anonfile_endpoint_url = server_list[server]

        # User specific api key
        self.api_key = '?token=' + api_key

        # Dev can set their own custom timeout as
        # to accommodate slower internet connections
        if custom_timeout is not None:
            self.timeout = custom_timeout
        else:
            # Set timeout (connect, read)
            self.timeout = (5, 5)
