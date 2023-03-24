import os
import unittest
from io import StringIO
import io
from datetime import datetime
from unittest.mock import patch
from generate_timesheet import getDate
from txt_style import bcolors

text = bcolors()

class TestClearConsole(unittest.TestCase):
    def teardown(self):
        os.name = 'posix'
        
    @patch('os.system')
    def test_clear_console_windows(self, mock_os_system):
        os.name = 'nt'
        getDate().clearConsole()
        mock_os_system.assert_called_once_with('cls')
    
    @patch('os.system')
    def test_clear_console_linux(self, mock_os_system):
        os.name = 'posix'
        getDate().clearConsole()
        mock_os_system.assert_called_once_with('clear')

class TestErrorMessage(unittest.TestCase):
    def setUp(self):
        self.get_date = getDate()
    
    def test_helpText(self):
        help_text = str('\x1b[95m' + 'NoTime' + '\x1b[0m' + '\n' +
            'Using with Notion time sheet recorded database to generating Excel time sheet' + '\n'*2 +
            '\x1b[95m' + '*** Command ***' + '\x1b[0m' + '\n' +
            '- ' + '\x1b[96m' + '\x1b[4m' + 'help' + '\x1b[0m' + '  : Showing help command' + '\n' +
            '- ' + '\x1b[96m' + '\x1b[4m' + 'exit' + '\x1b[0m' + '  : Exit the executing'   + '\n' +
            '- ' + '\x1b[96m' + '\x1b[4m' + 'clear' + '\x1b[0m' + ' : Clear input start date (Only useable while INPUT END DATE)' + '\n'*2 +
            '\x1b[95m' + '*** Support ***' + '\x1b[0m' + '\n' +
            'date format' + '\n' + 
            'dd-mm-yyyy' + '\n' +
            '\x1b[91m' + 'eg. ' + '\x1b[0m' + '\x1b[96m' + '\x1b[4m' + '22-08-2022' + '\x1b[0m' + '\n'*2
        )
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.get_date.helpText()
            self.assertEqual(output.getvalue(), help_text)
    
    def test_errorWrongDate(self):
        err_wrong_date_text = str('\x1b[91m' +
            'ValueError: Wrong date format or unsupported command' + '\x1b[0m' + '\n' +
            'Type "help" for hint command' + '\n'*2
        )
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.get_date.errorWrongDate()
            self.assertEqual(output.getvalue(), err_wrong_date_text)
    
    def test_errorEmptyText(self):
        err_empty_text = str('\x1b[91m' +
            'ValueError: Please enter date or command' + '\x1b[0m' + '\n' +
            'Type "help" for hint command' + '\n'*2
        )
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.get_date.errorEmptyText()
            self.assertEqual(output.getvalue(), err_empty_text)
    
    def test_endDateGreater(self):
        date = datetime.strptime('18-12-2023', '%d-%m-%Y')
        err_empty_text = str('\x1b[91m' + 
            'ValueError: End date should greater than ' + 
            '18-12-2023' + '\x1b[0m' + '\n'*2
        )
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.get_date.endDateGreater(date)
            self.assertEqual(output.getvalue(), err_empty_text)
    
    def test_showCompleteMessage(self):
        complete_msg = str('\x1b[92m' +
            'Generate timesheet completed!!' + '\x1b[0m' + '\n'*2
        )
        with patch('sys.stdout', new=io.StringIO()) as output:
            with patch('builtins.input', return_value=''):  # Mock user input
                self.get_date.showCompleteMessage()
        self.assertEqual(output.getvalue(), complete_msg)

class TestInputDate(unittest.TestCase):
    def setUp(self):
        self.input_date = getDate()
    
    def test_inputEndDate_valid(self):
        with patch('builtins.input', return_value=datetime(2022, 12, 19).strftime('%d-%m-%Y')) as output:
            self.input_date.inputEndDate()
        self.assertEq(output.getvalue())
    
if __name__ == '__main__':
    # print(datetime(2023, 12, 19).strftime('%d-%m-%Y'))
    unittest.main()

# \x1b[382 chars]-yyyy\n\x1b[91meg. \x1b[0m\x1b[96m\x1b[4m22-08-2022\x1b[0m\n\n
# \x1b[382 chars]-yyyy\n\x1b[91meg. \x1b[0m\x1b[96m\x1b[4m22-08-2022\x1b[0m\n'