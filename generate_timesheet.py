from datetime import datetime
from get_data import notionData as data
from txt_style import bcolors as text
from write_excel import GenerateExcel as generate_excel
import os

data = notionData()
generate_excel = GenerateExcel()
text = bcolors()

class getDate:
    def __init__(self) -> None:
        pass

    def clearConsole(self):
        '''Clear console log'''
        # windows os
        if str(os.name) == 'nt':
            os.system('cls')
        # other os
        else:
            os.system('clear')
    
    def getDate(self):
        '''Get date from console input'''
        self.clearConsole()
    # Start date
        start_date = self.inputStartDate()
        self.clearConsole()
    # End date
        end_date = self.inputEndDate(start_date)
        self.clearConsole()
        return start_date, end_date
    
    def inputStartDate(self) -> datetime:
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
                # type test
                elif str(input_date.upper()) == 'TEST' and retry_attempt < 3:
                    self.clearConsole()
                    print('Please input ' + text.UNDERLINE + text.HEADER + '"test"' + text.ENDC + ' again ' + text.FAIL + str(3-retry_attempt) + text.ENDC + ' time to entered test mode')
                    retry_attempt += 1
                    continue
                # when type test 3 times
                elif retry_attempt >= 3 and start_date != None and end_date != None:
                    start_date = datetime.strptime(str(start_date), '%d-%m-%Y')
                    end_date = datetime.strptime(str(end_date), '%d-%m-%Y')
                    self.clearConsole()
                    print(text.OKCYAN + 'Entering test mode...' + text.ENDC)
                    print('start date : ' + str(start_date))
                    print('end date   : ' + str(end_date))
                    time.sleep(3)
                    break
                # true date format
                else:
                    start_date = datetime.strptime(str(input_date), '%d-%m-%Y')
                    break
            # type wrong date format
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
                
                ''' and not use for unit testing '''
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
