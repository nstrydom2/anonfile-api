#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from .anonfile import *
from .anonfile import __version__


def main():
    parser = argparse.ArgumentParser(prog=package_name)
    parser._positionals.title = 'Commands'
    parser._optionals.title = 'Arguments'

    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('-V', '--verbose', default=True, action=argparse.BooleanOptionalAction, help="increase output verbosity")
    parser.add_argument('-l', '--logging', default=True, action=argparse.BooleanOptionalAction, help="enable URL logging")
    parser.add_argument('-t', '--token', type=str, default='secret', help="configure an API token (optional)")

    subparser = parser.add_subparsers(dest='command')
    upload_parser = subparser.add_parser('upload', help="upload a file to https://anonfiles.com")
    upload_parser.add_argument('-f', '--file', nargs='+', type=Path, help="one or more files to upload.", required=True)

    download_parser = subparser.add_parser('download', help="download a file from https://anonfiles.com")
    download_parser.add_argument('-u', '--url', nargs='+', type=str, help="one or more URLs to download", required=True)
    download_parser.add_argument('-p', '--path', type=Path, default=Path.cwd(), help="download directory (CWD by default)")

    try:
        args = parser.parse_args()
        anon = AnonFile(args.token)

        if args.command is None:
            raise UserWarning("missing a command")

        if args.command == 'upload':
            for file in args.file:
                upload = anon.upload(file, progressbar=args.verbose, enable_logging=args.logging)
                print(f"URL: {upload.url.geturl()}")

        if args.command == 'download':
            for url in args.url:
                download = anon.download(url, args.path, progressbar=args.verbose, enable_logging=args.logging)
                print(f"File: {download.file_path}")

    except UserWarning as bad_human:
        print(f"error: {bad_human}")
        parser.print_help(sys.stderr)
        sys.exit(2)
    except Exception as error:
        print(error, file=sys.stderr)


if __name__ == '__main__':
    main()
