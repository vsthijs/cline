from itertools import takewhile, repeat
import os, sys
from cline import __VERSION__


PROG: str = os.path.basename(sys.argv[0])


def error(msg: str):
    print(f"{PROG}: error: {msg}")
    exit(1)


def match_pattern(pattern: str, file: str) -> bool:
    if pattern == "*":
        return True
    elif pattern.count("*") == 2 and pattern.startswith("*") and pattern.endswith("*"):
        # pattern is surrounded with '*'
        return pattern.removeprefix("*").removesuffix("*") in file
    elif pattern.count("*") == 1:
        if pattern.startswith("*"):
            return file.endswith(pattern.removeprefix("*"))
        elif pattern.endswith("*"):
            return file.startswith(pattern.removesuffix("*"))
        else:  # '*' is somewhere in the middle
            start, stop = pattern.split("*")
            return file.startswith(start) and file.endswith(stop)
    elif "*" not in pattern:
        return file == pattern
    else:
        error(f"invalid pattern '{pattern}'.")


def rawbigcount(filename) -> int:
    """https://stackoverflow.com/a/27517681 - counts the amount of newlines"""
    f = open(filename, "rb")
    bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
    return sum(buf.count(b"\n") for buf in bufgen if buf)


def count_file(file: str) -> tuple[int, int]:
    return rawbigcount(file) + 1, 1


def count_directory(
    path: str, recursive: bool, pattern: str, include_hidden: bool
) -> tuple[int, int]:
    lines = 0
    files = 0
    for child in os.listdir(path):
        p = os.path.join(path, child)
        if child.startswith(".") and not include_hidden:
            pass  # skip
        elif os.path.isdir(p):
            if recursive:
                result = count_directory(p, True, pattern, include_hidden)
                lines += result[0]
                files += result[1]
        elif match_pattern(pattern, child):
            lines += count_file(p)[0]
            files += 1
    return lines, files


def usage():
    print(f"Usage:  {PROG} --help       Show this documentation.")
    print(f"        {PROG} --version    Show the version of {PROG}.")
    print(f"        {PROG} <files>       Count the total lines in the specified files.")
    print(f"        {PROG} <directories>  Count total lines of all files in the")
    print(f"                              specified directories.")
    print(f"                   -r | --recursive     Go into directories recursively.")
    print(f"")
    print(f"General flags:")
    print(f"        --fmt FMT           Output the number of lines in the specified")
    print(f"                            format. FMT is a string of which '%L' and")
    print(f"                            '%F' will be replaced with the amount of lines")
    print(f"                            and the amount of files respectively.")
    print(f"        --include-hidden    Includes files and directories whose names")
    print(f"                            begin with a '.'")
    print(f"        -p | --pattern PAT  Only count files which match the given")
    print(f"                            pattern.")


def version():
    print(f"{PROG} version {__VERSION__}, on Python version {sys.version}")


def main():
    if len(sys.argv) == 1:
        usage()
        error("no arguments given.")

    files: list[str] = []
    recursive: bool = False
    fmt: str | None = None
    pattern: str | None = None
    include_hidden: bool = False

    idx = 1
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        idx += 1
        if arg.startswith("-"):
            if arg in ["-r", "--recursive"]:
                recursive = True
            elif arg == "--fmt":
                if fmt is not None:
                    error("multiple formats given.")
                fmt = sys.argv[idx]
                idx += 1
            elif arg == "--include-hidden":
                if include_hidden:
                    print(f"{PROG}: warning: --include-hidden passed multiple times.")
                include_hidden = True
            elif arg in ["-p", "--pattern"]:
                if pattern is not None:
                    error("multiple patterns given.")
                pattern = sys.argv[idx]
                idx += 1
            elif arg in ["-h", "--help"]:
                usage()
                exit(0)
            elif arg in ["-v", "--version"]:
                version()
                exit(0)
            else:
                error(f"unknown flag {arg}.")
        elif os.path.exists(arg):
            files.append(arg)
        else:
            error(f"{arg} is not a file or a flag.")

    if fmt is None:
        fmt = "%L countend in %F files"

    if len(files) == 0:
        error("no files or directories given.")

    pattern = "*" if pattern is None else pattern

    counted_lines = 0
    counted_files = 0
    for p in files:
        if os.path.isdir(p):
            result = count_directory(p, recursive, pattern, include_hidden)
            counted_lines += result[0]
            counted_files += result[1]
        else:
            counted_lines += count_file(p)[0]

    print(
        fmt.replace("%L", str(counted_lines))
        .replace("%F", str(counted_files))
        .replace("\\n", "\n")
        .replace("\\t", "\t")
    )


if __name__ == "__main__":
    main()
