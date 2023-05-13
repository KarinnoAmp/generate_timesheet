import unittest
import json
from datetime import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from get_data import mathCalculator, setApi, notionData
'''
class testMathCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.mathCalculator = mathCalculator()

    def test_roundNumber_down(self):
        self.assertEqual(self.mathCalculator.roundNumber(float(0.001), 2), float(0.00))
    
    def test_roundNumber_up(self):
        self.assertEqual(self.mathCalculator.roundNumber(float(0.005), 2), float(0.01))
'''
class testSetApi(unittest.TestCase):
    def setUp(self) -> None:
        self.setApi = setApi()
    '''
    def test_setBody_withMoreThan_100_items(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        last_page:  str = 'Hello'
        expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-setBody_withMoreThan_100_items.json'))
        with open(expect_result_path, 'r') as expect_result_file:
            expect_result: dict = json.load(expect_result_file)
        self.assertDictEqual(self.setApi.setBody(start_date, end_date, person_key, last_page), expect_result)
    
    def test_sendRequest(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        self.setApi.setBody(start_date, end_date, person_key)
        expected_result: dict = {
            'object': 'list', 
            'results': [], 
            'next_cursor': None, 
            'has_more': False, 
            'type': 'page', 
            'page': {}
        }
        self.assertDictEqual(self.setApi.sendRequest(), expected_result)

    def test_sendRequest_withErrorUrl(self):
        url: str = 'https://api.notion.com/v1/databases/ffffffffffffffffffffffffffffffff'
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        self.setApi.setBody(start_date, end_date, person_key)
        with self.assertRaises(ConnectionError):
            self.setApi.sendRequest(url=url)
    
    def test_sendRequest_withHeaderError(self):
        header: dict = {
            'Authorization': 'Bearer ffffffffffffffffffffffff',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        self.setApi.setBody(start_date, end_date, person_key)
        with self.assertRaises(ConnectionError):
            self.setApi.sendRequest(headers=header)
    
    def test_sendRequest_withBodyError(self):
        body: dict = {'hello': 123}
        with self.assertRaises(ConnectionError):
            self.setApi.sendRequest(json_data=body)
    
    def test_setBodyGetPerson(self):
        expect_result: dict = {
            'filter': {
                'and': [
                    {
                        'property': 'Task type',
                        'select': {
                            'equals': 'Information'
                        }
                    },
                    {
                        'property': 'Date',
                        'date': {
                            'on_or_before': '2022-11-01'
                        }
                    },
                    {
                        'property': 'Date',
                        'date': {
                            'on_or_after': '2022-11-01'
                        }
                    }
                ]
            }
        }
        self.assertDictEqual(self.setApi.setBodyGetPerson(), expect_result) 
    
    def test_setBodyGetPerson_customDate_str(self):
        start_date: str = '2022-11-01'
        end_date: str = '2022-11-01'
        expect_result: dict = {
            'filter': {
                'and': [
                    {
                        'property': 'Task type',
                        'select': {
                            'equals': 'Information'
                        }
                    },
                    {
                        'property': 'Date',
                        'date': {
                            'on_or_before': '2022-11-01'
                        }
                    },
                    {
                        'property': 'Date',
                        'date': {
                            'on_or_after': '2022-11-01'
                        }
                    }
                ]
            }
        }
        self.assertDictEqual(self.setApi.setBodyGetPerson(start_date=start_date, end_date=end_date), expect_result)
    
    def test_setBodyGetPerson_customDate_datetime(self):
        with self.assertRaisesRegex(ValueError, expected_regex='start_date or end_date was in wrong type'):
            self.setApi.setBodyGetPerson(start_date=datetime(2022, 11, 1), end_date=datetime(2022, 11, 1))
    
    def test_sendRequestGetPerson(self):
        self.assertNoLogs(self.setApi.sendRequestGetPerson())
    '''
class testNotionData(unittest.TestCase):
    def setUp(self) -> None:
        self.notionData = notionData()
    '''
    def test_checkTaskTitle(self):
        title: list = [
            {
            "type":"text",
            "text":{
                "content":"TMP Standup Meeting",
                "link":None
            },
            "annotations":{
                "bold":False,
                "italic":False,
                "strikethrough":False,
                "underline":False,
                "code":False,
                "color":"default"
            },
            "plain_text":"TMP Standup Meeting",
            "href":None
            }
        ]
        expect_result: str = 'TMP Standup Meeting'
        self.assertEqual(self.notionData.checkTaskTitle(title), expect_result)
    
    def test_checkTaskTitle_empty_list(self):
        title: list = []
        self.assertEqual(self.notionData.checkTaskTitle(title), None)
    
    def test_checkDateFormat(self):
        true_format: str = '2022-09-01T09:00:00.000+07:00'
        expect_result: str = '01/09/2022'
        self.assertEqual(self.notionData.checkDateFormat(true_format), expect_result)
    
    def test_checkDateFormat_wrong_format(self):
        false_format: str = '09:00:00.000+07:00T2022-09-01'
        with self.assertRaises(ValueError):
            self.notionData.checkDateFormat(false_format)
    
    def test_checkDateFormat_onlyDate(self):
        false_format: str = '2023-05-03'
        expect_result: str = '03/05/2023'
        self.assertEqual(self.notionData.checkDateFormat(false_format), expect_result)
    
    def test_checkDateFormat_none(self):
        none_format = None
        none_str_format: str = 'None'
        self.assertEqual(self.notionData.checkDateFormat(none_format), None)
        self.assertEqual(self.notionData.checkDateFormat(none_str_format), None)
    
    def test_checkDateFormat_intArgument(self):
        int_format = int(9)
        with self.assertRaises(AttributeError):
            self.notionData.checkDateFormat(int_format)
    
    def test_checkDateFormat_floatArgument(self):
        float_format = float(9)
        with self.assertRaises(AttributeError):
            self.notionData.checkDateFormat(float_format)
    
    def test_checkDateFormat_datetimeArgument(self):
        datetime_format = datetime(2023, 5, 3)
        with self.assertRaises(AttributeError):
            self.notionData.checkDateFormat(datetime_format)
    
    def test_checkTaskProject(self):
        data_set: list = [
            {
            "id":"w]LR",
            "name":"TMP1",
            "color":"yellow"
            }
        ]
        expect_result: list = ['TMP1']
        self.assertListEqual(self.notionData.checkTaskProject(data_set), expect_result)
    
    def test_checkTaskProject_2_project(self):
        data_set: list = [
            {
            "id":"w]LR",
            "name":"TMP1",
            "color":"yellow"
            },
            {
            "id":"w]LR",
            "name":"TMP2",
            "color":"green"
            }
        ]
        expect_result: list = ['TMP1', 'TMP2']
        self.assertListEqual(self.notionData.checkTaskProject(data_set), expect_result)
    
    def test_checkTaskProject_no_project(self):
        data_set: list = []
        self.assertIsNone(self.notionData.checkTaskProject(data_set))
    def test_summaryTasks(self):
        # Data set
        data_set_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
        person_name: str = 'Nakarin Viyapron'
        with open(data_set_path, 'r') as data_file:
            json_data: dict = json.load(data_file)
        # Expect result
        expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-summaryTasks.json'))
        with open(expect_result_path, 'r') as expect_result_file:
            expect_result: dict = json.load(expect_result_file)
        self.assertDictEqual(self.notionData.summaryTasks(json_data=json_data, person_name=person_name), expect_result)
    
    def test_summaryTasks_withEmptyTasks(self):
        # Data set
        data_set_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
        person_name: str = 'Nakarin Viyapron'
        json_data: list = [
            {
                "object": "list",
                "results": [],
                "next_cursor": None,
                "has_more": False,
                "type": "page",
                "page": {},
                "developer_survey": "https://notionup.typeform.com/to/bllBsoI4?utm_source=postman"
            }
        ]
        # Expect result
        expect_result: dict = {
            'person': 'Nakarin Viyapron',
            'data': [],
            'total_work_hours': 0.0
        }
        self.assertDictEqual(self.notionData.summaryTasks(json_data=json_data, person_name=person_name), expect_result)
    
    def test_getTaskData(self):
        data_set = self.notionData.getTaskData(
            start_date=datetime(2022, 9, 1), 
            end_date=datetime(2022, 10, 31), 
            personal_id='fb6ab337-1d37-4efc-8730-efbe2c602a9f'
        )
        path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
        with open(path, 'r') as json_file:
            json_data: dict = json.load(json_file)
        self.assertListEqual(data_set, json_data)
    
    def test_getTaskData_wrong_argument_type(self):
        with self.assertRaises(AttributeError):
            self.notionData.getTaskData(
                start_date='2022, 9, 1', 
                end_date='2022, 10, 31', 
                personal_id='fb6ab337-1d37-4efc-8730-efbe2c602a9f'
            )

    def test_getPerson(self):
        path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getPerson.json'))
        with open(path, 'r') as json_file:
            data: dict = json.load(json_file)
        self.assertDictEqual(self.notionData.getPerson(), data)
'''
    def test_getProject(self):
        path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getProject.json'))
        with open(path, 'r') as json_file:
            data: dict = json.load(json_file)
        self.assertDictEqual(self.notionData.getProject(data['test_data']), data['expected_result'])

if __name__ == '__main__':
    unittest.main()
    