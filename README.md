# No TimeSheet
> *Version 1.1 Release*

## Version 1.1
### *New feature & improvement*
- This is release version
- Improve config.yaml file
---
## Version 1.0
### *New feature & improvement*
- Can run script generate with .exe file or .script file
- Build python script as .exe file on windows and .script in macos
---
## Version 0.3
### *New feature & improvement*
- Change name to No TimeSheet
- Can input date into console separately from config.yaml file
- Can type "help" for show hint command
- Can use command "exit" to exit the executing
- Show query date while getting Notion data
- Add more command while typing start/end date eg. -exit, -clear
- Adjust error message when typing unsupported command
- Adjust generated excel format
- Improve script function
### *Bug fix*
- Fixed error when input upper or title case command
---
## version 0.2B
### *New feature & improvement*
- Input query date from console
- Change progress bar loading color
- Adjust generated excel format
### *Bug fix*
- Fixed error when input wrong date format in console input
- Fixed console log blink on color change when loading success
---
## Version 0.1A
### *New feature & improvement*
- Generate excel of notion timesheet data
- Add more user id to config file
- Add color to progress bar
- Add http error message while send requests was failed
### *Bug fix*
- Fixed collect timesheet data with range more than 100 pages
- Fixed round the number with 2 decimal
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