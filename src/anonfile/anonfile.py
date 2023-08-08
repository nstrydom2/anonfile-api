#!/usr/bin/env python3

"""
The MIT License

Copyright (c) 2021, Nicholas Bruce Strydom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import annotations

import html
import logging
import os
import platform
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union
from urllib.parse import ParseResult, urljoin, urlparse
from urllib.request import getproxies

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from requests_toolbelt import MultipartEncoderMonitor, user_agent
from tqdm import tqdm
from urllib3 import Retry

__version__ = "1.0.0"
package_name = "anonfile"
python_major = "3"
python_minor = "8"

try:
    assert sys.version_info >= (int(python_major), int(python_minor))
except AssertionError:
    raise RuntimeError(f"{package_name!r} requires Python {python_major}.{python_minor}+ (You have Python {sys.version})")

#region logging

def get_config_dir() -> Path:
    """
    Return a platform-specific root directory for user configuration files.
    """
    default_dir = Path.home().joinpath('.config')
    return {
        'Windows': Path(os.path.expandvars('%LOCALAPPDATA%')),
        'Darwin': Path.home().joinpath('Library').joinpath('Application Support'),
        'Linux': default_dir
    }.get(platform.system(), default_dir).joinpath(package_name)

def get_logfile_path() -> Path:
    """
    Return a platform-specific log file path.
    """
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    log_file = config_dir.joinpath("anonfile.log")
    log_file.touch(exist_ok=True)
    return log_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s::%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(get_logfile_path())
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#endregion

@dataclass(frozen=True)
class ParseResponse:
    """
    Data class that is primarily used as a structured return type for the upload,
    preview and download methods.
    """
    response: Response
    file_path: Path
    ddl: ParseResult

    @property
    def json(self) -> dict:
        """
        Return the entire HTTP response.
        """
        return self.response.json()

    @property
    def status(self) -> bool:
        """
        Return the upload status. If `False`, an error message indicating the
        cause for the malfunction will be redirected to `sys.stderr`.
        """
        status = bool(self.json['status'])

        if not status:
            print(self.json['error']['message'], file=sys.stderr)
            print(self.json['error']['type'], file=sys.stderr)
            print(self.json['error']['code'], file=sys.stderr)

        return status

    @property
    def url(self) -> ParseResult:
        """
        Return the URL associated with the uploaded file.
        ```
        """
        return urlparse(self.json['data']['file']['url']['full'])

    #region metadata

    @property
    def id(self) -> str:
        """
        Return the ID (path) of the uploaded file.
        """
        return self.json['data']['file']['metadata']['id']

    @property
    def name(self) -> Path:
        """
        Return the filename of the uploaded file.
        """
        return Path(self.json['data']['file']['metadata']['name'])

    @property
    def size(self) -> int:
        """
        Return the uploaded file size in bytes.
        """
        return int(self.json['data']['file']['metadata']['size']['bytes'])

    @property
    def size_readable(self) -> str:
        """
        Return a human-readable file size in base 10.
        """
        return self.json['data']['file']['metadata']['size']['readable']

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ID={self.id})"

    #endregion

class AnonFile:
    """
    The unofficial Python API for https://anonfiles.com.

    Basic Usage
    -----------

    ```
    from anonfile import AnonFile

    anon = AnonFile()
    preview = anon.preview('https://anonfiles.com/b7NaVd0cu3/topsecret_mkv')

    # topsecret.mkv
    print(preview)
    ```
    """
    _timeout = (5, 5)
    _total = 5
    _status_forcelist = [413, 429, 500, 502, 503, 504]
    _backoff_factor = 1
    _user_agent = None
    _proxies = None

    API = "https://api.anonfiles.com/"

    __slots__ = ['endpoint', 'token', 'timeout', 'total', 'status_forcelist', 'backoff_factor', 'user_agent', 'proxies']

    def __init__(self,
                 token: str="undefined",
                 timeout: Tuple[float,float]=_timeout,
                 total: int=_total,
                 status_forcelist: List[int]=_status_forcelist,
                 backoff_factor: int=_backoff_factor,
                 user_agent: str=_user_agent,
                 proxies: dict=_proxies) -> AnonFile:
        self.token = token
        self.timeout = timeout
        self.total = total,
        self.status_forcelist = status_forcelist,
        self.backoff_factor = backoff_factor
        self.user_agent = user_agent
        self.proxies = proxies

    @staticmethod
    def __progressbar_options(iterable, desc, unit, color: str="\033[32m", char='\u25CB', total=None, disable=False) -> dict:
        """
        Return custom optional arguments for `tqdm` progressbars.
        """
        return {
            'iterable': iterable,
            'bar_format': "{l_bar}%s{bar}%s{r_bar}" % (color, "\033[0m"),
            'ascii': char.rjust(9, ' '),
            'desc': desc,
            'unit': unit.rjust(1, ' '),
            'unit_scale': True,
            'unit_divisor': 1024,
            'total': len(iterable) if total is None else total,
            'disable': not disable
        }

    @property
    def retry_strategy(self) -> Retry:
        """
        The retry strategy returns the retry configuration made up of the
        number of total retries, the status forcelist as well as the backoff
        factor. It is used in the session property where these values are
        passed to the HTTPAdapter.
        """
        return Retry(total=self.total, status_forcelist=self.status_forcelist, backoff_factor=self.backoff_factor)

    @property
    def session(self) -> Session:
        """
        Create a custom session object. A request session provides cookie
        persistence, connection-pooling, and further configuration options.
        """
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=self.retry_strategy))
        session.hooks['response'] = [lambda response, *args, **kwargs: response.raise_for_status()]
        session.headers.update({
            'User-Agent' : self.user_agent or user_agent(package_name, __version__)
        })
        return session

    def __get(self, url: str, **kwargs) -> Response:
        """
        Returns the GET request encoded in `utf-8`. Adds proxies to this session
        on the fly if urllib is able to pick up the system's proxy settings.
        """
        response = self.session.get(url, timeout=self.timeout, proxies=self.proxies or getproxies(), **kwargs)
        response.encoding = 'utf-8'
        return response

    @staticmethod
    def __callback(monitor: MultipartEncoderMonitor, tqdm_handler: tqdm):
        """
        Define a multi part encoder monitor callback function for the upload method.
        """
        tqdm_handler.total = monitor.len
        tqdm_handler.update(monitor.bytes_read - tqdm_handler.n)

    def upload(self, path: Union[str, Path], progressbar: bool=False, enable_logging: bool=False) -> ParseResponse:
        """
        Upload a file located in `path` to http://anonfiles.com. Set
        `enable_logging` to `True` to store the URL in a global config file.

        Example
        -------

        ```
        from anonfile import AnonFile

        anon = AnonFile('my_token')
        result = anon.upload('test.txt')

        # https://anonfiles.com/9ee1jcu6u9/test_txt
        print(result.url.geturl())
        ```

        Note
        ----
        Although `anonfile` offers unlimited bandwidth, uploads cannot exceed a
        file size of 20GB in theory. Due to technical difficulties in the implementation,
        the upper cap occurs much earlier at around 500MB.
        """
        path = Path(path)
        size = os.stat(path).st_size
        options = AnonFile.__progressbar_options(None, f"Upload: {path.name}", unit='B', total=size, disable=progressbar)
        with open(path, mode='rb') as file_handler:
            fields = {'file': (path.name, file_handler, 'application/octet-stream')}
            with tqdm(**options) as tqdm_handler:
                encoder_monitor = MultipartEncoderMonitor.from_fields(fields, callback=lambda monitor: AnonFile.__callback(monitor, tqdm_handler))
                response = self.session.post(
                    urljoin(AnonFile.API, 'upload'),
                    data=encoder_monitor,
                    params={'token': self.token},
                    headers={'Content-Type': encoder_monitor.content_type},
                    timeout=self.timeout,
                    proxies=getproxies(),
                    verify=True
                )
                logger.log(logging.INFO if enable_logging else logging.NOTSET, "upload::%s", response.json()['data']['file']['url']['full'])
                return ParseResponse(response, path, None)

    def preview(self, url: str, path: Union[str, Path]=Path.cwd()) -> ParseResponse:
        """
        Obtain meta data associated with this `url` without commiting to a time-
        consuming download.

        Example
        -------

        ```
        from anonfile import AnonFile

        anon = AnonFile()
        preview = anon.preview('https://anonfiles.com/P0mev3tfz7/topsecret_mp4')

        # File Size: 116271961B
        print(f"File Size: {preview.size}B")
        ```
        """
        with self.__get(urljoin(AnonFile.API, f"v2/file/{urlparse(url).path.split('/')[1]}/info")) as response:
            links = re.findall(r'''.*?(?:href|value)=['"](.*?)['"].*?''', html.unescape(self.__get(url).text), re.I)
            ddl = urlparse(next(filter(lambda link: 'cdn-' in link, links)))
            file_path = Path(path).joinpath(Path(ddl.path).name)
            return ParseResponse(response, file_path, ddl)

    def download(self, url: str, path: Union[str, Path]=Path.cwd(), progressbar: bool=False, enable_logging: bool=False) -> ParseResponse:
        """
        Download a file from https://anonfiles.com given a `url`. Set the download
        directory in `path` (uses the current working directory by default). Set
        `enable_logging` to `True` to store the URL in a global config file.

        Example
        -------

        ```
        from pathlib import Path
        from anonfile import AnonFile

        anon = AnonFile('my_token')
        target_dir = Path.home().joinpath('Downloads')
        result = anon.download("https://anonfiles.com/9ee1jcu6u9/test_txt", target_dir)
        # WindowsPath('C:/Users/username/Downloads/test.txt')
        print(result.file_path)
        ```

        Note
        ----
        The `anon.ddl` property stores a direct download link which is suitable
        for reading the response stream. In contrast, the URL defined in `anon.url.geturl()`
        is a better choice for sharing links.
        """
        MB = 1_048_576
        download = self.preview(url, path)

        options = AnonFile.__progressbar_options(None, f"Download {download.id}", unit='B', total=download.size, disable=progressbar)
        with open(download.file_path, mode='wb') as file_handler:
            with tqdm(**options) as tqdm_handler:
                with self.__get(download.ddl.geturl(), stream=True) as response:
                    for chunk in response.iter_content(chunk_size=1*MB):
                        tqdm_handler.update(len(chunk))
                        file_handler.write(chunk)

        logger.log(logging.INFO if enable_logging else logging.NOTSET, "download::%s", url)
        return download
