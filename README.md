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

Code coverage:
```
# automated testing coverage
coverage run -m pytest tests

# manual testing coverage
coverage run -m lpm

# create report
cd coverage_data
coverage combine
coverage html
open htmlcov/index.html
```

Upload to [PyPI](https://pypi.org/project/lpm/0.0.1/):
1. Update version in `lpm/__init__.py`
2. Run code linting and formatting
3. Update `requirements-dev.txt` if needed
4. Update `setup.py` if needed
5. Run tests to assure everything is working
6. `python -m build`
7. `python -m twine upload dist/*`


The folders and files for this project are as follows:
`lpm`: Contains source code for project.
`lpm/__main__.py`: Entry point for lpm.
`tests`: Folder containing tests.
`setup.py`: Python package setup.
