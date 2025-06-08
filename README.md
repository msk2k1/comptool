A platform-agnostic tool for comparing an internal drive to an external copy.

# Usage

Run from the command line: `python <folder>/comptool.py <args>`

By default (when passing no parameters), the script will attempt to compare everything in the two roots.
The folders that will be compared will be previewed before comparison is attempted.

## Arguments
- `-h` or `--help`: show this help message and exit
- `-s` or `--subfolder`: Path to a subfolder to compare, as opposed to the entirety of the drives.
    - Provide a path to the folder on one of the drive copies. The script attempts to extract the subfolder path from this and apply it to both roots. 
- `-l` or `--left-root`: Path to root of filesystem on left side of comparison.
- `-r` or `--right-root` or `--rite-root`: Path to root of filesystem on right side of comparison.
- `-n` or `--no-log`: Disable logging to output file.

## Return Codes
- 0 => success (no errors encountered)
- 1 => error during comparison
- 2 => error parsing input parameters

## Dependencies 
diff and meld on Linux; Winmerge on Windows

<!-- ----------------------------------------------------- -->

# Configuration

## Config File
Various settings can be pre-defined per machine in `comptool.config`, located in the **same folder** as the script:
- `left` and `rite`: the roots of the two file systems to compare.
- `logfile`: where to log comparisons when they are made on this machine.
- `ignores`: a string to represent files and folders to exclude from comparison. Separate entries with comma (`,`). End folders with double backslash (`\\`).
- `winmenge`: for windows machines, the path to the WinMerge executable. Use double backslashes in path.

Here is an example entry. `MSK-PC` is the name of the computer for which this configuration applies.
```
[MSK-PC]
left = F:\
rite = D:\
logfile = D:\comptool-log.txt
ignores = My*\\,desktop.ini,WindowsPowershell\\,Zoom\\
winmerge = C:\\Program Files\\WinMerge\\WinMergeU.exe
```

A configuration must at least include the left and right directories. The other options are only used if they are included (logfile, ignores) or necessary (winmerge, for Windows machines).

## Commandline Parameters
If provided, commandline parameters `--left-root` and `--rite-root` take priority over the config file.
This allows you to temporarily override one of them for a single comparison, instead of needing to edit the config file.

<!-- ----------------------------------------------------- -->

# Logs

Note that as written, the log file will only show the paths relative to the roots being used on that system.
This means an overall comparison (w/out specifying subfolder) will have just "/" for these runs.
You will need to know the left and right roots used at the time to deduce the full paths.

Logging can be disabled with the `--no-log` flag (see "Usage" section).