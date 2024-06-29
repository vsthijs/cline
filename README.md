# Cline

A flexible line counter utility

## Usage:

```sh
cline <files and directories> [flags]
        counts the lines of the specified files.
```

### Flags

- `--fmt <FMT>` - Output the number of lines in the specified format. FMT is a string of which '%L' and '%F' will be replaced with the amount of lines and the amount of files respectively.
- `--include-hidden` - Includes files and directories whose names begin with a '.'
- `-p | --pattern <PAT>` - Only count files which match the given pattern.
- `-r | --recursive` - Go into directories recursively.
