from datetime import datetime
from get_data import notionData
from txt_style import bcolors
from write_excel import GenerateExcel
import os


data = notionData()
generate_excel = GenerateExcel()
text = bcolors()

class getDate:  
    def __init__(self) -> None:
        pass
    
    
# Clear console log
    def clearConsole(self):
        if str(os.name) == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    
# Get date from console input
    def getDate(self):
        self.clearConsole()
    # Start date
        while True:
            try:
                print(text.HEADER + 'Input start date' + text.ENDC)
                print('Format: ddmmyyyy')
                input_date = input(text.OKBLUE + 'INPUT_DATE: ' + text.ENDC)
                # input_date = 21102022
                start_date = datetime.strptime(str(input_date), '%d%m%Y')
                break
            except ValueError:
                self.clearConsole()
                print(text.FAIL + text.BOLD + 'Error: Wrong date' + text.ENDC + '\n')
                continue
        self.clearConsole()
    # End date
        while True:
            try:
                print(text.OKGREEN + 'Start date:' + str(start_date.strftime('%d-%m-%Y')) + text.ENDC)
                print(text.HEADER + 'Input end date' + text.ENDC)
                print('Format: ddmmyyyy')
                input_date = input(text.OKBLUE + 'INPUT_DATE: ' + text.ENDC)
                end_date = datetime.strptime(str(input_date), '%d%m%Y')
                if end_date < start_date:
                    self.clearConsole()
                    print(text.FAIL + text.BOLD + 'Error: End date should greater than ' + str(start_date.strftime('%d-%m-%Y')) + text.ENDC + '\n')    
                    continue
                else:
                    break
            except ValueError:
                self.clearConsole()
                print(text.FAIL + text.BOLD + 'Error: Wrong date' + text.ENDC + '\n')
                continue
        self.clearConsole()
        return start_date, end_date

get_date = getDate()
startDate, endDate = get_date.getDate()
generate_excel.write_excel(data.getTasksData(str(startDate.date()), str(endDate.date())))
