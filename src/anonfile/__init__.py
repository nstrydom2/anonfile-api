#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from collections import namedtuple
from distutils.util import strtobool
from pathlib import Path
from typing import List

from .anonfile import *
from .anonfile import __version__


def __print_dict(dictionary: dict, indent: int = 4) -> None:
    print("{\n%s\n}" % '\n'.join([f"\033[36m{indent * ' '}{key}\033[0m: \033[32m{value}\033[0m" for key, value in dictionary.items()]))


def __from_file(path: Path) -> List[str]:
    with open(path, mode='r', encoding='utf-8') as file_handler:
        return [line.rstrip() for line in file_handler.readlines() if line[0] != '#']


def main():
    parser = argparse.ArgumentParser(prog=package_name)
    parser._positionals.title = 'Commands'
    parser._optionals.title = 'Arguments'

    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('-V', '--verbose', default=True, action='store_true', help="increase output verbosity (default)")
    parser.add_argument('--no-verbose', dest='verbose', action='store_false', help="run commands silently")
    parser.add_argument('-l', '--logging', default=True, action='store_true', help="enable URL logging (default)")
    parser.add_argument('--no-logging', dest='logging', action='store_false', help="disable all logging activities")
    parser.add_argument('-t', '--token', type=str, default='secret', help="configure an API token (optional)")
    parser.add_argument('-a', '--user-agent', type=str, default=None, help="configure custom User-Agent (optional)")

    subparser = parser.add_subparsers(dest='command')
    upload_parser = subparser.add_parser('upload', help="upload a file to https://anonfiles.com")
    upload_parser.add_argument('-f', '--file', nargs='+', type=Path, help="one or more files to upload.", required=True)

    preview_parser = subparser.add_parser('preview', help="read meta data from a file on https://anonfiles.com")
    preview_parser.add_argument('-u', '--url', nargs='+', type=str, help="one or more URLs to preview", required=True)

    download_parser = subparser.add_parser('download', help="download a file from https://anonfiles.com")
    download_parser.add_argument('-u', '--url', nargs='*', type=str, help="one or more URLs to download")
    download_parser.add_argument('-f', '--batch-file', type=Path, nargs='?', help="file containing URLs to download, one URL per line")
    download_parser.add_argument('-p', '--path', type=Path, default=Path.cwd(), help="download directory (CWD by default)")
    download_parser.add_argument('-c', '--check', default=True, action='store_true', help="check for duplicates (default)")
    download_parser.add_argument('--no-check', dest='check', action='store_false', help="disable checking for duplicates")

    log_parser = subparser.add_parser('log', help="access the anonfile logger")
    log_parser.add_argument('--reset', action='store_true', help="reset all log file entries")
    log_parser.add_argument('--path', action='store_true', help="return the log file path")
    log_parser.add_argument('--read', action='store_true', help='read the log file')

    try:
        args = parser.parse_args()
        anon = AnonFile(args.token, user_agent=args.user_agent)

        if args.command is None:
            raise UserWarning("missing a command")

        if args.user_agent is not None:
            anon.user_agent = args.user_agent

        if args.command == 'upload':
            for file in args.file:
                upload = anon.upload(file, progressbar=args.verbose, enable_logging=args.logging)
                print(f"URL: {upload.url.geturl()}")

        if args.command == 'preview':
            for url in args.url:
                preview = anon.preview(url)
                values = ['online' if preview.status else 'offline', preview.file_path.name, preview.url.geturl(), preview.ddl.geturl(), preview.id, f"{preview.size}B"]

                if args.verbose:
                    __print_dict(dict(zip(['Status', 'File Path', 'URL', 'DDL', 'ID', 'Size'], values)))
                else:
                    print(','.join(values))

        if args.command == 'download':
            for url in (args.url or __from_file(args.batch_file)):
                download = lambda url: anon.download(url, args.path, progressbar=args.verbose, enable_logging=args.logging)

                if args.check and anon.preview(url, args.path).file_path.exists():
                    print(f"\033[33mWarning:\033[0m A file with the same name already exists in {str(args.path)!r}.")
                    choice = input("Proceed with download? [Y/n] ")
                    if choice == '' or strtobool(choice):
                        print(f"File: {download(url).file_path}")
                else:
                    print(f"File: {download(url).file_path}")

        if args.command == 'log':
            if args.reset:
                open(get_logfile_path(), mode='w', encoding='utf-8').close()
            if args.path:
                print(get_logfile_path())
            if args.read:
                with open(get_logfile_path(), mode='r', encoding='utf-8') as file_handler:
                    log = file_handler.readlines()

                    if not log:
                        msg = "Nothing to read because the log file is empty"
                        print(f"\033[33m{'[ WARNING ]'.ljust(12, ' ')}\033[0m{msg}")
                        return

                    parse = lambda line: line.strip('\n').split('::')
                    Entry = namedtuple('Entry', 'timestamp method url')

                    tabulate = "{:<19} {:<8} {:<30}".format

                    print(f"\033[32m{tabulate('Date', 'Method', 'URL')}\033[0m")

                    for line in log:
                        entry = Entry(parse(line)[0], parse(line)[1], parse(line)[2])
                        print(tabulate(entry.timestamp, entry.method, entry.url))

    except UserWarning as bad_human:
        print(f"error: {bad_human}")
        parser.print_help(sys.stderr)
        sys.exit(2)
    except Exception as error:
        print(error, file=sys.stderr)


if __name__ == '__main__':
    main()
