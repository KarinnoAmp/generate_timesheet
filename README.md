# No Time Sheet
> *Version 2.0.1*
---
## Requirements
> Python script for generating timesheet from

1. First, output requirements.txt to a file.

```bash
pip freeze > requirements.txt
```
2. Create a new python environment
### Windows
```bash
python -m venv Environment
```
### MacOS or Linux
```bash
python3 -m venv Environment
```

3. Copy or move this requirements.txt to another environment and install with it.

```bash
pip install -r requirements.txt
```
4. How to build python script to .exe or script file
```bash
pyinstaller --onefile file.py
```
