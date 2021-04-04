# User Guide

See `lpm -h`:

```
usage: lpm [-h] [-s] [-v] [--reset] [--settings] [languages [languages ...]]

Lines Per Minute, a typing tool made for programmers.

positional arguments:
  languages      List of programming languages to filter code snippets. Must be one of a python, java, javascript. If no languages provided, all languages are loaded by default.

optional arguments:
  -h, --help     show this help message and exit
  -s, --stats    Display the lifetime statistics and the statistics from the 5 most recent completed snippets.
  -v, --version  Get program version.
  --reset        Prompts the user if they would like to reset the config, stats, and/or redownload the code snippets.
  --settings     Edit lpm settings via default text editor.

Example usage:
    lpm
    lpm python
    lpm java
    lpm python java
    lpm --help
    lpm --stats
```
