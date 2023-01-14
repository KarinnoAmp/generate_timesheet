from datetime import datetime
from get_data import notionData as data
from txt_style import bcolors as text
from write_excel import GenerateExcel as generate_excel
import os



class getDate:
    def clearConsole(self) -> None:
        '''Clear console log'''
        # windows os
        if str(os.name) == 'nt':
            os.system('cls')
        # other os
        else:
            os.system('clear')
    
    
    
    def getDate(self, start_date=None, end_date=None) -> datetime:
        '''Get date from console input'''
        self.clearConsole()
        if start_date != None and end_date != None:
            start_date = datetime.strptime(str(start_date), '%d-%m-%Y')
            end_date = datetime.strptime(str(end_date), '%d-%m-%Y')
        else:
        # Input start date
            while True:
                try:
                    # input start date
                    input_date: str = input(text.WARNING + 'INPUT_START_DATE: ' + text.ENDC)
                    # type help
                    if str(input_date.upper()) == 'HELP':
                        self.helpText()
                        continue
                    # type exit
                    elif str(input_date.upper()) == 'EXIT':
                        self.clearConsole()
                        exit()
                    # type none
                    elif str(input_date) == str():
                        self.clearConsole()
                        self.errorEmptyText()
                        continue
                    else:
                        start_date = datetime.strptime(str(input_date), '%d-%m-%Y')
                    break
                # type wrong date format
                except ValueError:
                    self.clearConsole()
                    self.errorWrongDate()
                    continue
            self.clearConsole()
        # Input End date
            while True:
                try:
                    # show start date
                    print(text.OKGREEN + 'Start date: ' + str(start_date.strftime('%d-%m-%Y')) + text.ENDC)
                    # input end date
                    input_date: str = input(text.WARNING + 'INPUT_END_DATE: ' + text.ENDC)
                    # type help
                    if str(input_date.upper()) == 'HELP':
                        self.helpText()
                        continue
                    # type clear
                    elif str(input_date.upper()) == 'CLEAR':
                        start_date, end_date = self.getDate()
                        break
                    # type exit
                    elif str(input_date.upper()) == 'EXIT':
                        self.clearConsole()
                        exit()
                    # type none
                    elif str(input_date) == str():
                        self.clearConsole()
                        self.errorEmptyText()
                        continue
                    else:
                        end_date = datetime.strptime(str(input_date), '%d-%m-%Y')
                    # type end date before start date
                    if end_date < start_date:
                        self.clearConsole()
                        self.endDateGreater(start_date)
                        continue
                    else:
                        break
                # type wrong date format
                except ValueError:
                    self.clearConsole()
                    self.errorWrongDate()
                    continue
            self.clearConsole()
        print('start : ' + str(start_date))
        print('end   : ' + str(end_date))
        return start_date, end_date
    
    
    
    def helpText(self) -> None:
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
    
    
    
    def errorWrongDate(self) -> None:
        print(text.FAIL +
              'ValueError: Wrong date format or unsupported command' + text.ENDC + '\n' +
              'Type "help" for hint command' + '\n'
        )
        
        
        
    def errorEmptyText(self) -> None:
        print(text.FAIL + 
              'ValueError: Please enter date or command' + text.ENDC + '\n'
              'Type "help" for hint command' + '\n'
        )
    
    
    
    def endDateGreater(self, start_date) -> None:
        print(text.FAIL + 
              'ValueError: End date should greater than ' + 
              str(start_date.strftime('%d-%m-%Y')) + text.ENDC + '\n'
        )
    
    def showCompleteMessage(self) -> None:
        print(text.OKGREEN +
              'Generate timesheet completed!!' + text.ENDC + '\n'
        )
        input('Press Enter to continue')
        self.clearConsole()
    
    
    
    
if __name__ == '__main__':
    startDate, endDate = getDate().getDate('01-11-2022', '30-11-2022')
    generate_excel().write_excel(data().getTasksData(startDate, endDate))
    getDate().clearConsole()
    getDate().showCompleteMessage()
