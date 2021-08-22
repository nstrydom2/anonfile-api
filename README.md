<p align="center">
  <a href="https://github.com/nstrydom2/anonfile-api" title="Project Logo">
    <img height="150" style="margin-top:15px" src="https://raw.githubusercontent.com/nstrydom2/anonfile-api/master/logo.svg">
  </a>
</p>

# Anonfiles.com Unofficial Python API

[![PyPI version shields.io](https://img.shields.io/pypi/v/anonfile)](https://pypi.python.org/pypi/anonfile/)
[![CI](https://github.com/nstrydom2/anonfile-api/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/nstrydom2/anonfile-api/actions/workflows/python-package.yml)
[![PyPI download total](https://img.shields.io/pypi/dm/anonfile)](https://pypi.python.org/pypi/anonfile/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/anonfile)](https://pypi.python.org/pypi/anonfile/)
[![PyPI license](https://img.shields.io/pypi/l/anonfile)](https://pypi.python.org/pypi/anonfile/)


This unofficial Python API was created to make uploading and downloading files
from <anonfiles.com> simple and effective for programming in Python. The goal of
the project is to create an intuitive library for anonymous file sharing.

## Getting Started

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. See deployment for notes on how to
deploy the project on a live system.

### Prerequisites

Python 3.7+ is required to run this application, other than that there are no
prerequisites for the project, as the dependencies are included in the repository.

### Installing

To install the library is as simple as running

```bash
pip install anonfile
```

from the command line. To install this library in debug mode, use

```bash
pip install -e .
```

instead. It is recommended to create an virtual environment prior
to installing this library.

### Dev Notes

Run unit tests locally:

```bash
pytest --verbose -s [--token "REDACTED"]
```

Add the `-k test_*` option if you want to test only a single function.

## Usage

Import the module and instantiate the `AnonFile()` constructor. Setting the download
directory in `path` is optional. Using the API `token` in the constructor is optional
as well. A valid `token` registers all file uploads online, i.e. a list of all uploaded
files is made accessible to any user that [signs into your account](https://anonfiles.com/login).

```python
from anonfile import AnonFile

anon = AnonFile()

# upload a file and enable progressbar terminal feedback
upload = anon.upload('/home/guest/jims_paperwork.doc', progressbar=True)
print(upload.url.geturl())

# download a file and set the download directory
from pathlib import Path
target_dir = Path.home().joinpath('Downloads')
filename = anon.download("https://anonfiles.com/9ee1jcu6u9/test_txt", path=target_dir)
print(filename)
```

And voilà, pain-free anonymous file sharing. If you want more information about
the `AnonFile` API visit [anonfiles.com](https://anonfiles.com/docs/api).

## Command Line Interface

```bash
# get help
anonfile [download|upload] --help

# note: both methods expect at least one argument, but can take on more
anonfile download --url https://anonfiles.com/93k5x1ucu0/test_txt
anonfile upload --file ./test.txt
```

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Http for Humans
* [TQDM](https://github.com/tqdm/tqdm) - Fast & Extensible Progress Bars
* [anonfiles.com](https://anonfiles.com/docs/api) - AnonFiles.com REST API

## Versioning

Navigate to [tags on this repository](https://github.com/nstrydom2/anonfile-api/tags)
to see all available versions.

## Authors

| Name             | Mail Address                | GitHub Profile                                |
|------------------|-----------------------------|-----------------------------------------------|
| Nicholas Strydom | nstrydom@gmail.com          | [nstrydom2](https://github.com/nstrydom2)     |
| hentai-chan      | dev.hentai-chan@outlook.com | [hentai-chan](https://github.com/hentai-chan) |

See also the list of [contributors](https://github.com/nstrydom2/anonfile-api/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## Acknowledgments

* Joseph Marie Jacquard
* Charles Babbage
* Ada Lovelace
* My Dad
* Hat tip to anyone whose code was used
* Inspiration
* etc
