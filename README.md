# Notion Timesheet generator
*Version 0.2B*
>version 0.2B*
## Release note
### New feature & improvement
- Input query date from console
- Change progress bar loading color
- Adjust generated excel format
### Bug fix
- Fixed error when input wrong date format in console input
- Fixed console log blink on color change when loading success
---
>version 0.1A*
## Release note
### New feature & improvement
- Generate excel of notion timesheet data
- Add more user id to config file
- Add color to progress bar
- Add http error message while send requests was failed
### Bug fix
- Fixed collect timesheet data with range more than 100 pages
- Fixed round the number with 2 decimal
---
## Requirements
> Python script for generating timesheet from

1. First, output requirements.txt to a file.

```bash
pip freeze > requirements.txt
```

2. Copy or move this requirements.txt to another environment and install with it.

```bash
pip install -r requirements.txt
```
