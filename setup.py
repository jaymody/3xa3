"""Setup script for lpm."""

import os
import runpy

from setuptools import setup


def get_version():
    """Reads current lpm version from disk."""
    filename = os.path.join(os.path.dirname(__file__), "lpm", "__init__.py")
    var = runpy.run_path(filename)
    return var["__version__"]


_VERSION = get_version()

setup(
    name="lpm",
    version=_VERSION,
    entry_points={
        "console_scripts": ["lpm=lpm.__main__:main"],
    },
    description="Command line application for practicing coding speed.",
    author="Jay Mody, Jessica Lim, Maanav Dalal",
    author_email="jaykmody@gmail.com, jessicalim813@gmail.com, maanavdalal@gmail.com",
    packages=["lpm"],
    package_dir={"lpm": "lpm"},
    package_data={"lpm": ["data/examples.json.gz"]},
    include_package_data=True,
    url="https://gitlab.cas.mcmaster.ca/modyj/3xa3.git",
    license="https://www.gnu.org/licenses/agpl-3.0.html",
    long_description=open("README.md").read(),
    install_requires=["setuptools"],
    zip_safe=True,
    test_suite="tests",
    keywords=["lpm", "typing", "typist", "code", "keyboard"],
    platforms=["unix", "linux", "osx", "cygwin"],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
