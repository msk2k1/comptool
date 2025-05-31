# comptool

A platform-agnostic tool for comparing an internal drive to an external copy.

### Usage

Run from the command line: `python <folder>/comptool.py <args>`

By default (when passing no parameters), the script will attempt to compare everything in the two roots.
The folders that will be compared will be previewed before comparison is attempted.

**Arguments:**
`-h`, `--help`                  show this help message and exit
`-s`, `--subfolder` SUBFOLDER   Path to a subfolder to compare.

**Return codes:**
- 0 => success (no errors encountered)
- 1 => error during comparison
- 2 => error with input parameters
- 3 => error parsing config file

**Dependencies:** linux: diff and meld; windows: winmerge

### Configuration

Define roots of internal data drive, and where external data drive is mounted, in `comptool.config`. This file should be in the **same folder** as the script.

The config file can have unique entries for different computers by name. Here is an example entry:
```
[MSK-PC]
left = F:\
rite = D:\
logfile = D:\comptool-log.txt
ignores = My*\\,desktop.ini,WindowsPowershell\\,Zoom\\
winmerge = C:\\Program Files\\WinMerge\\WinMergeU.exe
```

Configuration options are:
- `left` and `rite`: the roots of the two file systems to compare.
- `logfile`: where to log comparisons when they are made on this machine.
- `ignores`: a string to represent files and folders to exclude from comparison. Separate entries with comma (`,`). End folders with double backslash (`\\`).
- `winmenge`: for windows machines, the path to the WinMerge executable. Use double backslashes in path.

### Logs

Note that as written, the log file will only show the paths relative to the roots being used on that system.
This means an overall comparison (w/out specifying subfolder) will have just "/" for these runs.
You will need to know the left and right roots used at the time to deduce the full paths.