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
        start_date = self.inputStartDate()
        self.clearConsole()
        end_date = self.inputEndDate(start_date)
        self.clearConsole()
        return start_date, end_date
    
    def inputStartDate(self) -> datetime:
        while True:
            try:
                input_date = input(text.WARNING + 'INPUT_START_DATE: ' + text.ENDC)
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
        return start_date  
        
    def inputEndDate(self, start_date: datetime=None) -> datetime:
        if not start_date:
            ''' For unit testing '''
            start_date = datetime(2022, 12, 18)
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
                
                ''' and not use for unit testing '''
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
        return end_date 
        
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
            'ValueError: Please enter date or command' + text.ENDC + '\n' +
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
        input('Press Enter to continue')
        self.clearConsole()
    
if __name__ == '__main__':
    getDate().clearConsole()
    startDate, endDate = getDate().getDate()
    generate_excel.new_write_excel(data.getAllTasksDataNew(startDate, endDate))
    getDate().clearConsole()
    getDate().showCompleteMessage()
