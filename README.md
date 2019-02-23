# Anonfile.com Unofficial Python API

This unofficial Python API was created to make uploading and downloading files from Anonfile.com simple, and effective for programming in Python. The goal of the project is to create an intuitive library for anonymous file sharing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3 is required to run this application, other than that there are no prerequisites for the project, as the dependencies are included in the repo along with a virtual environment.

### Installing

To install the library, is as simple as cloning the repo and then importing the module.

Simply clone the repository.

```
git clone https://github.com/nstrydom2/anonfile-api.git
```

And have fun!

```
import anonfile

anon = AnonFile()
file_info = anon.upload('/home/guest/jims_paperwork.doc')
```

## Usage

Just import the module, and then instantiate the AnonFile() object. Finally, start uploading.

```
import anonfile

anon = AnonFile()
file_info = anon.upload('/home/guest/jims_paperwork.doc')

anon.download(file_info)
```

And viola, pain free anonymous file sharing. Working towards proxying as well. If you want some info on the returning json object(its going to be the "file" object). Visit [Anonfile.com](https://anonfile.com/docs/api).

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Http for Humans
* [Anonfile.com](https://anonfile.com/docs/api) - AnonFile.com REST API

## Versioning

For the versions available, see the [tags on this repository](https://github.com/nstrydom2/anonfile-api/tags). 

## Authors

* **Nicholas Strydom** - nstrydom@gmail.com - [nstrydom2](https://github.com/nstrydom2)

See also the list of [contributors](https://github.com/nstrydom2/anonfile-api/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Joseph Marie Jacquard
* Charles Babbage
* Ada Lovelace
* My Dad
* Hat tip to anyone whose code was used
* Inspiration
* etc

