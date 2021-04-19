# Lines Per Minute

A command-line typing tool made for programmers. Inspired by [wpm](https://github.com/cslarsen/wpm).

## Install
Requires `python>=3.6`:
```
pip install lpm
```

## Usage
Start the program with:
```
lpm
```
Use `lpm -h` for additional options.

## Dev Notes

Install dev dependencies:
```shell
pip install -r requirements-dev.txt
```

Run tests:
```shell
pytest tests
```

Code formatting:
```shell
black setup.py lpm/*.py tests/*.py
```

Code linting:
```shell
pylint setup.py lpm/*.py tests/*.py
```

Create documentation:
```shell
cd docs
make clean && make html && make latexpdf
```

Code coverage:
```shell
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

* `Doc/`: Project documentation and deliverables (ie SRS, TestPlan, TestReport, etc ...)

* `docs/`: Sphinx auto-generated source code.

* `lpm/`: Contains source code for project.
    * `lpm/__main__.py`: Entry point for lpm.
    * `lpm/commandline.py`: CLI code.
    * `lpm/config.py`: Configuration.
    * `lpm/game.py`: Typing interface game controller.
    * `lpm/screen.py`: Commandline IO via curses.
    * `lpm/snippets.py`: Data classes for code snippets.
    * `lpm/stats.py`: Statistics calculations and classes.

* `ProjectSchedule/`: Gantt Chart.

* `tests/`: Automated unit tests.

* `setup.py`: Python package setup.
