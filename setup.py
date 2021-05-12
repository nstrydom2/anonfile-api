import re

from setuptools import find_packages, setup

with open("src/anonfile/anonfile.py", encoding='utf-8') as file_handler:
    lines = file_handler.read()
    version = re.search(r'__version__ = "(.*?)"', lines).group(1)
    package_name = re.search(r'package_name = "(.*?)"', lines).group(1)
    python_major = int(re.search(r'python_major = "(.*?)"', lines).group(1))
    python_minor = int(re.search(r'python_minor = "(.*?)"', lines).group(1))

print("reading dependency file")

with open("requirements/release.txt", mode='r', encoding='utf-8') as requirements:
    packages = requirements.read().splitlines()

with open("requirements/dev.txt", mode='r', encoding='utf-8') as requirements:
    dev_packages = requirements.read().splitlines()

print("reading readme file")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=version,
    author="Nicholas Strydom",
    author_email="nstrydom@gmail.com",
    description="An unofficial library that wraps the anonfile.com REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nstrydom2/anonfile-api",
    project_urls={
        'Source Code': "https://github.com/nstrydom2/anonfile-api",
        'Bug Reports': "https://github.com/nstrydom2/anonfile-api/issues",
        'Changelog': "https://github.com/nstrydom2/anonfile-api/blob/master/CHANGELOG.md"
    },    
    python_requires=">=%d.%d" % (python_major, python_minor),
    install_requires=packages,
    extra_requires={
        'dev': dev_packages[1:],
        'test': ['pytest']
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': ['%s=%s.__init__:main' % (package_name, package_name)]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="anonfile rest api"
)

wheel_name = package_name.replace('-', '_') if '-' in package_name else package_name
print("\033[92mSetup is complete. Run 'python -m pip install dist/%s-%s-py%d-none-any.whl' to install this wheel.\033[0m" % (wheel_name, version, python_major))
