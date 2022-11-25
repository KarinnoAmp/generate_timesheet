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
    
    
    
    def clearConsole(self):
        '''Clear console log'''
        if str(os.name) == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    
    
    def getDate(self):
        '''Get date from console input'''
        self.clearConsole()
    # Start date
        while True:
            try:
                input_date = input(text.WARNING + 'INPUT_START_DATE: ' + text.ENDC)
                # input_date = '01-09-2022'
                if str(input_date.upper()) == 'HELP':
                    self.helpText()
                    continue
                elif str(input_date.upper()) == 'EXIT':
                    self.clearConsole()
                    exit()
                elif str(input_date) == str():
                    self.clearConsole()
                    self.errorEmptyText()
                    continue
                else:
                    start_date = datetime.strptime(str(input_date), '%d-%m-%Y')
                break
            except ValueError:
                self.clearConsole()
                self.errorWrongDate()
                continue
        self.clearConsole()       
    # End date
        while True:
            try:
                print(text.OKGREEN + 'Start date: ' + str(start_date.strftime('%d-%m-%Y')) + text.ENDC)
                input_date = input(text.WARNING + 'INPUT_END_DATE: ' + text.ENDC)
                if str(input_date.upper()) == 'HELP':
                    self.helpText()
                    continue
                elif str(input_date.upper()) == 'CLEAR':
                    start_date, end_date = self.getDate()
                    break
                elif str(input_date.upper()) == 'EXIT':
                    self.clearConsole()
                    exit()
                elif str(input_date) == str():
                    self.clearConsole()
                    self.errorEmptyText()
                    continue
                else:
                    end_date = datetime.strptime(str(input_date), '%d-%m-%Y')
                
                if end_date < start_date:
                    self.clearConsole()
                    self.endDateGreater(start_date)
                    continue
                else:
                    break
            except ValueError:
                self.clearConsole()
                self.errorWrongDate()
                continue
        self.clearConsole()
        return start_date, end_date
    
    
    
    def helpText(self):
        self.clearConsole()
        print(text.HEADER + 'NoTime' + text.ENDC + '\n' +
              'Using with Notion time sheet recorded database to generating Excel time sheet' + '\n'*2 +
              text.HEADER + '*** Command ***' + text.ENDC + '\n' +
              '- ' + text.OKCYAN + text.UNDERLINE + 'help' + text.ENDC + '  : Showing help command' + '\n' +
              '- ' + text.OKCYAN + text.UNDERLINE + 'exit' + text.ENDC + '  : Exit the executing'   + '\n' +
              '- ' + text.OKCYAN + text.UNDERLINE + 'clear' + text.ENDC + ' : Clear input start date (Only useable while INPUT END DATE)' + '\n'*2 +
              text.HEADER + '*** Support ***' + text.ENDC + '\n' +
              'date format' + '\n' + 
              'dd-mm-yyyy' + '\n' +
              text.FAIL + 'eg. ' + text.ENDC + text.OKCYAN + text.UNDERLINE + '22-08-2022' + text.ENDC + '\n'
        )
    
    
    
    def errorWrongDate(self):
        print(text.FAIL +
              'ValueError: Wrong date format or unsupported command' + text.ENDC + '\n' +
              'Type "help" for hint command' + '\n'
        )
        
        
        
    def errorEmptyText(self):
        print(text.FAIL + 
              'ValueError: Please enter date or command' + text.ENDC + '\n'
              'Type "help" for hint command' + '\n'
        )
    
    
    
    def endDateGreater(self, start_date):
        print(text.FAIL + 
              'ValueError: End date should greater than ' + 
              str(start_date.strftime('%d-%m-%Y')) + text.ENDC + '\n'
        )
    
    def showCompleteMessage(self):
        print(text.OKGREEN +
              'Generate timesheet completed!!' + text.ENDC + '\n'
        )
    
    
if __name__ == '__main__':
    getDate().clearConsole()
    startDate, endDate = getDate().getDate()
    generate_excel.write_excel(data.getTasksData(startDate, endDate))
    getDate().clearConsole()
    getDate().showCompleteMessage()
