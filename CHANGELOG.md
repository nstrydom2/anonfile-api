# Changelog

## Version 0.2.7 (2021-8-31)

Makes further improvements to the CLI:

- implements a `--batch-file` option for the download method
- adds a `--check` (for duplicates) option to the download method; this can be disabled
  with the `--no-check` method. It's enabled by default and may require further
  user-input in case the target directory contains a file with the same name as
  the issued download command
- implements a preview command to obtain meta data without committing to a time-
  consuming download

As for the main library, the following changes have been added since the last release:

- the `ParseResponse` data class now contains a `ddl` field; it contains a direct
  download link if this structured was returned by a download method, else `None`
- the default token was renamed from `""` to `"undefined"`. This change has no effect
  that would require any further actions from you
- implements the preview command that's also callable from the CLI
- updates some remarks in the doc string
- the implementation for issuing requests has been improved here and there

## Version 0.2.6 (2021-8-21)

Adds the `enable_logging` parameter to the upload and download method. This feature
stores the target URL in a global configuration file. It's located in

- **Windows:** `%LOCALAPPDATA%/anonfile`
- **Darwin:** `$HOME/Library/Application Support/anonfile`
- **Linux:** `$HOME/.config/anonfile`

There are two functions you can use to easily access these paths in code:

```python
from anonfile import get_config_dir, get_logfile_path

config_dir, logfile = get_config_dir(), get_logilfe_path()

print(f"{config_dir=}\n{logfile=}")
```

This feature is turned off by default in the library, and turned on by default
in the built-in CLI. Furthermore, the `--verbose` option is now also turned on by
default in the CLI; if that's something you don't want you can turn it off again
using the `--no-verbose` flag.

## Version 0.2.5 (2021-7-28)

- Updates requests and requests-toolbelt dependencies
- Modified test_anonfile.py to be more robust by adding a test for .mkv video format (see also: #50 )

## Version 0.2.4 (2021-5-13)

- **NOTE** Version `0.2.3` was skipped due to a technical mistake
- Adds a rudimentary CLI
- Removes `requests_html` as dependency and improves download performance
- Adds `tqdm` progressbar support to `upload` and `download`

```bash
# get help
anonfile [download|upload] --help

# 1. enable verbose for progressbar feedback, else run silent
# 2. both methods expect at least one argument

anonfile --verbose download --url https://anonfiles.com/93k5x1ucu0/test_txt

anonfile --verbose upload --file ./test.txt
```

- Upgrades `faker` dependency from 8.1.2 to 8.1.3

## Version 0.2.2 (2021-5-05)

- **NOTE** Version `0.2.1` was skipped due to a technical mistake
- Unit Tests are now compatible with Python 3.7
- Upgrades `importlib-metadata` dependency to version 4.0.1 in `requirements/release.txt`
- Fixes an error in `setup.py`

## Version 0.2.0 (2021-05-04)

- **IMPORTANT:** This is a major update to the client-facing library interface
  and project infrastructure, see below a small code snippet to help you migrate
  to the newest version of `anonfile`:

```diff
# flat namespace
- from anonfile.anonfile import AnonFile
+ from anonfile import AnonFile

anon = AnonFile('my_token')

# new method names
- upload = anon.upload_file('/home/guest/jims_paperwork.doc')
+ upload = anon.upload('/home/guest/jims_paperwork.doc')

- download = anon.download_file('https://anonfiles.com/9ee1jcu6u9/test_txt')
+ download = anon.download('https://anonfiles.com/9ee1jcu6u9/test_txt')
```

- The return type of the `upload` and `download` method changed to the `ParseResponse`
  dataclass
- Drops support for all third-party servers, i.e. only file up- and downloads to
  anonfiles.com work out of the box
- Reduces all project dependencies to `requests`, `requests_html` and `faker`
- Added doc strings everywhere

## Version 0.1.3 (2021-04-02)

- Added a retry strategy to HTTP requests and updated the `lxml` dependency

## Version 0.1.2 (2020-06-28)

- Changed the URI for the target API's from 'https://example.com/api' to 'https://api.example.com/'.
- Fix bug where hosting website was returning a 404.
