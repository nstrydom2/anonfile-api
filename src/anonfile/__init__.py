#!/usr/bin/env python3

import argparse
from pathlib import Path

from .anonfile import *
from .anonfile import __version__

def main():
    parser = argparse.ArgumentParser(prog=package_name)
    subparser = parser.add_subparsers(dest='command')

    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('--verbose', action='store_true', help="increase output verbosity")
    parser.add_argument('--token', type=str, default='secret', help="configure an API token (optional)")

    upload_parser = subparser.add_parser('upload', help="upload a file to https://anonfiles.com")
    upload_parser.add_argument('--file', nargs='+', type=Path, help="one or more file to upload.")

    download_parser = subparser.add_parser('download', help="download a file from https://anonfiles.com")
    download_parser.add_argument('--url', nargs='+', type=str, help="one or more URL to download")
    download_parser.add_argument('--path', type=Path, default=Path.cwd(), help="download directory (CWD by default)")

    args = parser.parse_args()

    anon = AnonFile(args.token)

    if args.command == 'upload':
        for file in args.file:
            upload = anon.upload(file, progressbar=args.verbose)
            print(f"URL: {upload.url.geturl()}")

    if args.command == 'download':
        for url in args.url:
            download = anon.download(url, args.path, progressbar=args.verbose)
            print(f"File: {download.file_path}")


if __name__ == '__main__':
    main()
