# Cline

A flexible line counter utility

- [Usage](#usage)
    - [Flags](#flags)
- [Install](#install)

## Usage:

```sh
cline <files and directories> [flags]
        counts the lines of the specified files.
```

### Flags

- `--fmt <FMT>` - Output the number of lines in the specified format. FMT is a string of which '%L' and '%F' will be replaced with the amount of lines and the amount of files respectively.
- `--include-hidden` - Includes files and directories whose names begin with a '.'
- `-p | --pattern <PATTERN>` - Only count files which match the given pattern.
- `-r | --recursive` - Go into directories recursively.

## Install

To install the tool from source, first clone this repo. In the repo, run:

```sh
$ python -m build
```

This requires the build package to be installed with pip. This can be done with `pip install build`.
To install the built package locally, run:

```sh
$ pip install dist/cline-<VERSION>-py3-none-any.whl
```

Now, the `cline` tool is installed and on path.
