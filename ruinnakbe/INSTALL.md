# How to Install and Build ruinnakbe

This document provides instructions on how to build the `ruinnakbe` application from source and create a release archive.

## Prerequisites

- Python 3
- `pip` (Python package installer)

## 1. Install Dependencies

You will need to install the `pyinstaller` package to build the executable. You can install it using `pip`:

```bash
pip3 install pyinstaller
```

## 2. Build the Executable

To build the executable, run the following command from the root of the project:

```bash
cd ruinnakbe
pyinstaller --onefile main.py
```

This will create a `dist` directory containing the executable file named `main`.

## 3. Create a Release Archive

To create a release archive, you can create a compressed tarball of the executable.

First, create a `release` directory:
```bash
mkdir release
```

Then, create the archive:
```bash
tar -czvf release/ruinnakbe.tar.gz -C dist main
```

The release archive will be located at `release/ruinnakbe.tar.gz`.

## 4. Run the Application

You can run the application directly from the executable created in the `dist` folder:

```bash
./dist/main
```

Or, you can extract the archive and run it from there:

```bash
tar -xzvf release/ruinnakbe.tar.gz
./main
```
