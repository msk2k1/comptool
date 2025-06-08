A platform-agnostic tool intended to facilitate comparisons between an internal drive and an external copy.

Comptool has no comparison logic of its own. Instead, I wrote this script as a single tool to easily request and log comparisons:
- On Linux, diff is called for a quick, high-level comparison. Meld is then used if the user wants to manually inspect further.
- On Windows, the script simply calls WinMerge.

<!-- ----------------------------------------------------- -->

# Usage
A recent release of Python is required to run this script.
You'll also need installs of diff and meld when on Linux, or WinMerge when on Windows. These are the programs called to perform comparisons.

Comptool requires a "left" and "right" directory to compare. In practice, I use the "left" for what's stored in my hard drive, and the "right" for an external backup on a USB drive. 
This is not the only way it could be used, but it helps to be consistent with whatever method you choose.

The "left" and "right" directories can be passed in one of two ways:
1. Using a [preset configuration](#config-file), or
2. Using [runtime parameters](#command-line-arguments) `--left-root` and `--right-root`.

Running `comptool --help` lists all available commandline parameters. They're also described in the appropriate sections throughout this document.

<!-- ----------------------------------------------------- -->

# Configuration

## Config File
It's expected that a pre-defined configuration is made for each computer you intend to run Comptool on.
These are stored in `comptool.config`, which should be in the same folder as the script.
The configuration can define several settings:
- `left` and `rite`: The roots of the two file systems to compare. These are **required** for each configuration.
- `logfile`: Path to text file to log comparisons in when they are made on this machine. 
    - The path to the containing folder is validated; if not found, the log is not performed.
- `ignores`: A string to represent files and folders to exclude from comparison. 
    - Separate entries with comma (`,`). End folder names with double backslash (`\\`).
    - If the ignores string is malformed, a warning will be shown, but comparison can still be made **without ignoring anything**.
- `winmerge`: For Windows machines, this is the path to the WinMerge executable. Use double backslashes in path.

Here's an example config file entry. `MSK-PC` is the name of the computer for which this configuration applies.
It compares items in internal drive `F:\` with copies on external drive `D:\`. Logs are stored on the external drive. 
```
[MSK-PC]
left = F:\
rite = D:\
logfile = D:\comptool-log.txt
ignores = My*\\,desktop.ini,WindowsPowershell\\,Zoom\\
winmerge = C:\\Program Files\\WinMerge\\WinMergeU.exe
```

## Command Line Arguments
Use the `--left-root` and `--right-root` directories to define left and right root paths at runtime. These take precedence over the "defaults" provided in the config file.

Note that, if you don't have a config file entry for your machine, logging and ignore pattern functionality is not accessible.
This is because `--left-root` and `--right-root` are intended to *temporarily* override definitions from the config file.

## Using Subfolders
By default, the script will attempt to compare everything in the two roots.
However, the `--subfolder` flag can be used to specify a single subfolder to compare instead.
To use, provide a **full path** to the folder on either of the drive copies. 

The script will attempt to extract the subfolder path, and apply it to both roots.
For example, if your roots are `C:\` and `D:\files\`, passing `--subfolder C:\documents\2025\` will attempt to compare `C:\documents\2025\` to `D:\files\documents\2025\`.
I did it this way to make passing subfolders easier through tab-completion.

To ensure the subfolder paths are parsed correctly, the comparison targets are shown before attempting a comparison.
This allows the user to review them manually.
Comptool also validates each of the paths it parses, and cancels the comparison if one of them doesn't exist.
 
<!-- ----------------------------------------------------- -->

# Output

## Return Codes
- 0 => success (no errors encountered)
- 1 => error during comparison
- 2 => error parsing input parameters

## Logs
The log file lists the paths compared relative to the roots being used on that system.
This means an overall comparison (without specifying subfolder) will have just "/" for these runs.
If a subfolder was specified, the path to just the subfolder (without either root) is listed.
The computer name is included in the log, so you can use your config file to deduce full paths if necessary.

Passing `--no-log` at runtime will always disable logging.