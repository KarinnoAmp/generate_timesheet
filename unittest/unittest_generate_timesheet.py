import os
import unittest
from unittest.mock import patch
import io
from io import StringIO
from datetime import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from txt_style import bcolors
from generate_timesheet import getDate

text = bcolors()

class TestClearConsole(unittest.TestCase):
    def teardown(self):
        os.name = 'posix'
        
    @patch('os.system')
    def test_clear_console_windows(self, mock_os_system):
        os.name = 'nt'
        with patch('sys.stdout', new=StringIO()):
            getDate().clearConsole()
            mock_os_system.assert_called_once_with('cls')
    
    @patch('os.system')
    def test_clear_console_linux(self, mock_os_system):
        os.name = 'posix'
        with patch('sys.stdout', new=StringIO()):
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
    
    def test_inputStartDate_valid(self):
        output_terminal: str = '\x1b[93mINPUT_START_DATE: \x1b[0m'
        with patch('sys.stdout', new=io.StringIO()) as terminal:
            with patch('sys.stdin', StringIO(datetime(2022, 12, 18).strftime('%d-%m-%Y'))):
                date = self.input_date.inputStartDate()
        self.assertEqual(terminal.getvalue(), output_terminal)
        self.assertEqual(date, datetime(2022, 12, 18))
        
    def test_inputStartDate_invalidDate(self):
        with patch('sys.stdout', new=StringIO()):
            with patch('sys.stdin', StringIO('123')):
                with self.assertRaises(EOFError):
                    self.input_date.inputStartDate()
    
    def test_inputEndDate_startDate_exit(self):
        with patch('sys.stdout', new=StringIO()):
            with patch('sys.stdin', StringIO('exit')):
                with self.assertRaises(SystemExit):
                    self.input_date.inputStartDate()
    
    def test_inputEndDate_valid(self):
        output_terminal: str = '\x1b[92mStart date: 18-12-2022\x1b[0m\n\x1b[93mINPUT_END_DATE: \x1b[0m'
        with patch('sys.stdout', new=io.StringIO()) as terminal:
            with patch('sys.stdin', StringIO(datetime(2022, 12, 19).strftime('%d-%m-%Y'))):
                date = self.input_date.inputEndDate()
        self.assertEqual(terminal.getvalue(), output_terminal)
        self.assertEqual(date, datetime(2022, 12, 19))
    
    def test_inputEndDate_invalidDate(self):
        with patch('sys.stdout', new=StringIO()):
            with patch('sys.stdin', StringIO('123')):
                with self.assertRaises(EOFError):
                    self.input_date.inputEndDate()
    
    def test_inputEndDate_startDate_greater_than_endDate(self):
        with patch('sys.stdout', new=StringIO()):
            with patch('sys.stdin', StringIO(datetime(2022, 12, 19).strftime('%d-%m-%Y'))):
                with self.assertRaises(EOFError):
                    self.input_date.inputEndDate(datetime(2023, 12, 19))
    
    def test_inputEndDate_endDate_exit(self):
        with patch('sys.stdout', new=StringIO()):
            with patch('sys.stdin', StringIO('exit')):
                with self.assertRaises(SystemExit):
                    self.input_date.inputEndDate()
                    # self.input_date.inputEndDate()
        
if __name__ == '__main__':
    unittest.main()
