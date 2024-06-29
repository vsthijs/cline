from itertools import takewhile, repeat
import os, sys


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
        print(f"{sys.argv[0]}: error: invalid pattern '{pattern}'.")
        exit(1)


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


def usage(prog: str):
    print(f"Usage:  {prog} --help       Show this documentation.")
    print(f"        {prog} --version    Show the version of {prog}.")
    print(f"        {prog} <files>       Count the total lines in the specified files.")
    print(f"        {prog} <directories>  Count total lines of all files in the")
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


def main():
    if len(sys.argv) == 1:
        print(f"{sys.argv[0]}: error: no arguments given.")
        usage(sys.argv[0])
        exit(1)

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
                    print(f"{sys.argv[0]}: error: multiple formats given.")
                    exit(1)
                fmt = sys.argv[idx]
                idx += 1
            elif arg == "--include-hidden":
                if include_hidden:
                    print(
                        f"{sys.argv[0]}: warning: --include-hidden passed multiple times."
                    )
                include_hidden = True
            elif arg in ["-p", "--pattern"]:
                if pattern is not None:
                    print(f"{sys.argv[0]}: error: multiple patterns given.")
                    exit(1)
                pattern = sys.argv[idx]
                idx += 1
            else:
                print(f"{sys.argv[0]}: error: unknown flag {arg}.")
                exit(1)
        elif os.path.exists(arg):
            files.append(arg)
        else:
            print(f"{sys.argv[0]}: error: {arg} is not a file or a flag.")
            return 1

    if fmt is None:
        fmt = "%L countend in %F files"

    if len(files) == 0:
        print(f"{sys.argv[0]}: error: no files or directories given.")
        exit(1)

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
