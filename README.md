# Anonfiles.com Unofficial Python API

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

To install the library is as simple as cloning the repository and running

```bash
pip install -e .
```

It is recommended to create an virtual environment prior to installing this library.
Alternatively, you can also install this library via Pip:

```bash
pip install anonfile
```

And have fun!

### Dev Notes

Run unit tests locally:

```bash
pytest --verbosity=2 -s --token "REDACTED"
```

Add the `-k test_*` option if you want to test only a single function.

## Usage

Import the module and instantiate the `AnonFile()` constructor. Setting the download
directory in `path` is optional.

```python
from anonfile import AnonFile

anon = AnonFile('api_key')

# uploading a file
upload = anon.upload('/home/guest/jims_paperwork.doc')
print(upload.url.geturl())

# downloading a file
from pathlib import Path

target_dir = Path.home().joinpath('Downloads')
filename = anon.download("https://anonfiles.com/9ee1jcu6u9/test_txt", path=target_dir)
print(filename)
```

And voilà, pain-free anonymous file sharing. If you want more information about
the `AnonFile` API visit [anonfiles.com](https://anonfiles.com/docs/api).

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Http for Humans
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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md)
license file for more details.

## Acknowledgments

* Joseph Marie Jacquard
* Charles Babbage
* Ada Lovelace
* My Dad
* Hat tip to anyone whose code was used
* Inspiration
* etc
