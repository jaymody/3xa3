# Lines Per Minute

Team Name: Lines Per Minute (lpm)

Team Members: Jay Mody, Jessica Lim, Maanav Dalal

This project is a reimplementation of [github.com/cslarsen/wpm](https://github.com/cslarsen/wpm).

## Install
```
pip install lpm
```

## Run
```
lpm
```

## Dev Setup

Install dev dependencies:
```
pip install -r requirements-dev.txt
```

Run tests:
```
pytest tests
```

Code formatting:
```
black setup.py lpm/*.py
```

Code linting:
```
pylint setup.py lpm/*.py
```

Install editable package:
```
pip install -e .
```

Create documentation:
```
cd docs
make clean && make html && make latexpdf
```

Upload to [PyPI](https://pypi.org/project/lpm/0.0.1/):
1. Update version in `lpm/__init__.py`
2. Update requirements-dev.txt if needed
3. Update setup.py if needed
4. Run tests to assure everything is working
5. `python -m build`
6. `python -m twine upload dist/*`


The folders and files for this project are as follows:
`lpm`: Contains source code for project.
`lpm/__main__.py`: Entry point for lpm.
`tests`: Folder containing tests.
`setup.py`: Python package setup.
