#!/usr/bin/env python3

def pytest_addoption(parser):
    parser.addoption(
        '--token',
        action='append',
        default=None,
        help="Secret anonfiles.com API token."
    )

def pytest_generate_tests(metafunc):
    if 'token' in metafunc.fixturenames:
        metafunc.parametrize('token', metafunc.config.getoption('token'))
