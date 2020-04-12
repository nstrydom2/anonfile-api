import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='anonfile-api',
    version='0.1',
    scripts=['anonfile_api'],
    author="Nicholas Strydom",
    author_email="nstrydom@gmail.com",
    description="An unofficial library that wraps the Anonfile.com REST Api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nstrydom2/anonfile-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
