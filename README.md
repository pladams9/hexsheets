# HexSheets
[![Version](https://img.shields.io/github/v/release/pladams9/hexsheets)](https://github.com/pladams9/hexsheets/releases)
![Last Commit](https://img.shields.io/github/last-commit/pladams9/hexsheets)

## What is HexSheets?
HexSheets is a basic spreadsheet application with hexagonal cells and a pet project of mine.
It was inspired by this post: http://www.secretgeek.net/hexcel.

![Screenshot](/screenshots/main-screen.PNG)

## Getting HexSheets

### Option 1: "Compiled" Release

*Currently only for Windows*

1. Go to [Releases](https://github.com/pladams9/hexsheets/releases) and download a ZIP file of
the latest release.
2. Unzip the archive.
3. Open `hexsheets-x.x.x.exe`

### Option 2: From Source
*Assumes you have some understanding of git .*
1. Clone the repository* to your local machine.
2. From the base directory, run `pip install -r requirements.txt`. Optionally, create a `venv`.
3. From the `/doc_src`, run `mkdocs build` to build the documentation (under the `/src/docs/` folder.)
4. From `/src` run `python hex-spreadsheet.py` to start HexSheets.

\* There are two main branches in the repository: `master`, which represents the most recent "stable"
release, and `develop`, which houses the most recent development version.

## Building HexSheets
If you have the HexSheets source code on your local machine, you can run `python build.py` from the
base directory, and it will build (or re-build) the documentation (using `mkdocs`) and then freeze
the python code into an executable file (using `pyinstaller`). The resulting files will be placed in
`/dist`. This has currently only been tested on a Windows 10 machine - if you are able to successfully
build on another OS, please let me know!
