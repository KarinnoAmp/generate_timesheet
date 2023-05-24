import unittest
import json
from datetime import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from get_data import mathCalculator, setApi, notionData
"""
class testMathCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.mathCalculator = mathCalculator()

    def test_roundNumber_down(self):
        self.assertEqual(self.mathCalculator.roundNumber(float(0.001), 2), float(0.00))
    
    def test_roundNumber_up(self):
        self.assertEqual(self.mathCalculator.roundNumber(float(0.005), 2), float(0.01))

class testSetApi(unittest.TestCase):
    def setUp(self) -> None:
        self.setApi = setApi()
    
    def test_setBodyNEW(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-setBody.json'))
        with open(expect_result_path, 'r') as expect_result_file:
            expect_result: dict = json.load(expect_result_file)
        output_result: dict = self.setApi.setBodyNew(start_date, end_date)
        try:
            self.assertDictEqual(output_result, expect_result)
            with open(expect_result_path, 'w') as json_export:
                json.dump(output_result, json_export, indent=4)
        except:
            pass
    
    def test_setBodyNEW_withMoreThan_100_items(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        last_page:  str = 'Hello'
        expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-setBody_withMoreThan_100_items.json'))
        with open(expect_result_path, 'r') as expect_result_file:
            expect_result: dict = json.load(expect_result_file)
        output_result: dict = self.setApi.setBodyNew(start_date, end_date, last_page)
        try:
            self.assertDictEqual(output_result, expect_result)
            with open(expect_result, 'w') as json_export:
                json.dump(output_result, json_export, indent=4)
        except:
            pass
        
    def test_sendRequest(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        self.setApi.setBodyNew(start_date, end_date)
        expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-sendRequest.json'))
        with open(expect_result_path, 'r') as expect_result_file:
            expect_result: dict = json.load(expect_result_file)
        output_result = self.setApi.sendRequest()
        self.assertDictEqual(output_result, expect_result)

    def test_sendRequest_withErrorUrl(self):
        url: str = 'https://api.notion.com/v1/databases/ffffffffffffffffffffffffffffffff'
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        self.setApi.setBodyNew(start_date, end_date)
        with self.assertRaises(ConnectionError):
            self.setApi.sendRequest(url=url)
    
    # def test_setBodyGetPerson(self):
    #     expect_result: dict = {
    #         'filter': {
    #             'and': [
    #                 {
    #                     'property': 'Task type',
    #                     'select': {
    #                         'equals': 'Information'
    #                     }
    #                 },
    #                 {
    #                     'property': 'Date',
    #                     'date': {
    #                         'on_or_before': '2022-11-01'
    #                     }
    #                 },
    #                 {
    #                     'property': 'Date',
    #                     'date': {
    #                         'on_or_after': '2022-11-01'
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    #     self.assertDictEqual(self.setApi.setBodyGetPerson(), expect_result) 
    
    # def test_setBodyGetPerson_customDate_str(self):
    #     start_date: str = '2022-11-01'
    #     end_date: str = '2022-11-01'
    #     expect_result: dict = {
    #         'filter': {
    #             'and': [
    #                 {
    #                     'property': 'Task type',
    #                     'select': {
    #                         'equals': 'Information'
    #                     }
    #                 },
    #                 {
    #                     'property': 'Date',
    #                     'date': {
    #                         'on_or_before': '2022-11-01'
    #                     }
    #                 },
    #                 {
    #                     'property': 'Date',
    #                     'date': {
    #                         'on_or_after': '2022-11-01'
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    #     self.assertDictEqual(self.setApi.setBodyGetPerson(start_date=start_date, end_date=end_date), expect_result)
    
    # def test_setBodyGetPerson_customDate_datetime(self):
    #     with self.assertRaisesRegex(ValueError, expected_regex='start_date or end_date was in wrong type'):
    #         self.setApi.setBodyGetPerson(start_date=datetime(2022, 11, 1), end_date=datetime(2022, 11, 1))
    
    # def test_sendRequestGetPerson(self):
    #     self.assertNoLogs(self.setApi.sendRequestGetPerson())
    
"""
class testNotionData(unittest.TestCase):
    def setUp(self) -> None:
        self.notionData = notionData()
        
    # def test_checkTaskTitle(self):
    #     title: list = [
    #         {
    #         "type":"text",
    #         "text":{
    #             "content":"TMP Standup Meeting",
    #             "link":None
    #         },
    #         "annotations":{
    #             "bold":False,
    #             "italic":False,
    #             "strikethrough":False,
    #             "underline":False,
    #             "code":False,
    #             "color":"default"
    #         },
    #         "plain_text":"TMP Standup Meeting",
    #         "href":None
    #         }
    #     ]
    #     expect_result: str = 'TMP Standup Meeting'
    #     self.assertEqual(self.notionData.checkTaskTitle(title), expect_result)
    
    # def test_checkTaskTitle_empty_list(self):
    #     title: list = []
    #     self.assertEqual(self.notionData.checkTaskTitle(title), None)
    
    # def test_checkDateFormat(self):
    #     true_format: str = '2022-09-01T09:00:00.000+07:00'
    #     expect_result: str = '01/09/2022'
    #     self.assertEqual(self.notionData.checkDateFormat(true_format), expect_result)
    
    # def test_checkDateFormat_wrong_format(self):
    #     false_format: str = '09:00:00.000+07:00T2022-09-01'
    #     with self.assertRaises(ValueError):
    #         self.notionData.checkDateFormat(false_format)
    
    # def test_checkDateFormat_onlyDate(self):
    #     false_format: str = '2023-05-03'
    #     expect_result: str = '03/05/2023'
    #     self.assertEqual(self.notionData.checkDateFormat(false_format), expect_result)
    
    # def test_checkDateFormat_none(self):
    #     none_format = None
    #     none_str_format: str = 'None'
    #     self.assertEqual(self.notionData.checkDateFormat(none_format), None)
    #     self.assertEqual(self.notionData.checkDateFormat(none_str_format), None)
    
    # def test_checkDateFormat_intArgument(self):
    #     int_format = int(9)
    #     with self.assertRaises(AttributeError):
    #         self.notionData.checkDateFormat(int_format)
    
    # def test_checkDateFormat_floatArgument(self):
    #     float_format = float(9)
    #     with self.assertRaises(AttributeError):
    #         self.notionData.checkDateFormat(float_format)
    
    # def test_checkDateFormat_datetimeArgument(self):
    #     datetime_format = datetime(2023, 5, 3)
    #     with self.assertRaises(AttributeError):
    #         self.notionData.checkDateFormat(datetime_format)
    
    # def test_checkTaskProject(self):
    #     data_set: list = [
    #         {
    #         "id":"w]LR",
    #         "name":"TMP1",
    #         "color":"yellow"
    #         }
    #     ]
    #     expect_result: list = ['TMP1']
    #     self.assertListEqual(self.notionData.checkTaskProject(data_set), expect_result)
    
    # def test_checkTaskProject_2_project(self):
    #     data_set: list = [
    #         {
    #         "id":"w]LR",
    #         "name":"TMP1",
    #         "color":"yellow"
    #         },
    #         {
    #         "id":"w]LR",
    #         "name":"TMP2",
    #         "color":"green"
    #         }
    #     ]
    #     expect_result: list = ['TMP1', 'TMP2']
    #     self.assertListEqual(self.notionData.checkTaskProject(data_set), expect_result)
    
    # def test_checkTaskProject_no_project(self):
    #     data_set: list = []
    #     self.assertIsNone(self.notionData.checkTaskProject(data_set))
    
    # def test_formattedTasks(self):
    #     test_data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData-Result.json')
    #     with open(test_data_file, 'r') as json_file:
    #         test_data: list = json.load(json_file)
    #     result_data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-formattedTasks-Result.json')
    #     with open(result_data_file, 'r') as json_file:
    #         result_data: list = json.load(json_file)
    #     output_result: list = self.notionData.formattedTasks(test_data)
    #     try:
    #         self.assertListEqual(output_result, result_data)
    #         with open(result_data_file, 'w') as json_export:
    #             json.dump(output_result, json_export, indent=4)
    #     except:
    #         pass
    
    # # def test_summaryTasks(self):
    # #     # Set Up
    # #     path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getProject.json'))
    # #     with open(path, 'r') as json_file:
    # #         data: dict = json.load(json_file)
    # #     self.notionData.getProject(data['test_data'])
    # #     # Data set
    # #     data_set_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
    # #     person_name: str = 'Nakarin Viyapron'
    # #     with open(data_set_path, 'r') as data_file:
    # #         tasks_data: dict = json.load(data_file)
    # #     # Expect result
    # #     expect_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-summaryTasks.json'))
    # #     with open(expect_result_path, 'r') as expect_result_file:
    # #         expected_result: dict = json.load(expect_result_file)
    # #     # Testing
    # #     result_data = self.notionData.summaryTasks(json_data=tasks_data, person_name=person_name)
    # #     self.assertDictEqual(result_data, expected_result)
    
    # def test_summaryTasksNEW(self):
    #     test_data_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-formattedTasks-Result.json'))
    #     with open(test_data_path, 'r') as test_data_file:
    #         test_data: dict = json.load(test_data_file)
    #     test_result_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-summaryTasks-Result.json'))
    #     with open(test_result_path, 'r') as json_result_file:
    #         result_data: dict = json.load(json_result_file)
    #     output_result: dict = self.notionData.summaryTasksNew(test_data)
    #     try:
    #         self.assertDictEqual(output_result, result_data)
    #         with open(test_result_path, 'w') as json_export:
    #             json.dump(output_result, json_export, indent=4)
    #     except:
    #         pass    
        
    def test_summaryTasks_withEmptyTasks(self):
        # Data set
        json_data: list = [{}]
        expect_result: dict = {}
        self.assertDictEqual(self.notionData.summaryTasksNew(json_data=json_data), expect_result)
    
    # def test_summaryTasks_one_project(self):
    #     # Set Up
    #     path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-summaryTasks-OneProject.json'))
    #     with open(path, 'r') as json_file:
    #         data: dict = json.load(json_file)
    #     self.notionData.getProject(data['test_data'])
    #     # Data set
    #     data_set_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
    #     person_name: str = 'Nakarin Viyapron'
    #     with open(data_set_path, 'r') as data_file:
    #         tasks_data: dict = json.load(data_file)
    #     # Testing
    #     result_data = self.notionData.summaryTasks(json_data=tasks_data, person_name=person_name)
    #     self.assertDictEqual(result_data, data['expected_result'])
    
    # def test_getTaskData(self):
    #     data_set = self.notionData.getTaskData(
    #         start_date=datetime(2022, 9, 1), 
    #         end_date=datetime(2022, 10, 31), 
    #         personal_id='fb6ab337-1d37-4efc-8730-efbe2c602a9f'
    #     )
    #     path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData_summaryTasks.json'))
    #     with open(path, 'r') as json_file:
    #         json_data: dict = json.load(json_file)
    #     self.assertListEqual(data_set, json_data)
    
    def test_getTaskDataNEW(self):
        output_result: list = self.notionData.getTaskDataNew(
            start_date=datetime(2024, 4, 3), 
            end_date=datetime(2024, 4, 3)
        )
        path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData-Result.json'))
        with open(path, 'r') as json_file:
            json_data: dict = json.load(json_file)
        try:
            self.assertListEqual(output_result, json_data)
            with open(path, 'w') as json_export:
                json.dump(output_result, json_export, indent=4)
        except:
            pass
    
    def test_getTaskDataNEW_withEmptyResult(self):
        output_result: list = self.notionData.getTaskDataNew(
            start_date=datetime(2020, 4, 3), 
            end_date=datetime(2020, 4, 3)
        )
        result_file_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getTaskData-EmptyResult.json'))
        with open(result_file_path, 'r') as json_file:
            json_data: dict = json.load(json_file)
        try:
            self.assertListEqual(output_result, json_data)
            with open(result_file_path, 'w') as json_export:
                json.dump(output_result, json_export, indent=4)
        except:
            pass
    
    # def test_getTaskData_wrong_argument_type(self):
    #     with self.assertRaises(AttributeError):
    #         self.notionData.getTaskData(
    #             start_date='2022, 9, 1', 
    #             end_date='2022, 10, 31', 
    #             personal_id='fb6ab337-1d37-4efc-8730-efbe2c602a9f'
    #         )
            
    # def test_getPerson(self):
    #     path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getPerson.json'))
    #     with open(path, 'r') as json_file:
    #         data: dict = json.load(json_file)
    #     self.assertDictEqual(self.notionData.getPerson(data['test_data']), data['expected_result'])
    
    # def test_getProject(self):
    #     path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/get_data-getProject.json'))
    #     with open(path, 'r') as json_file:
    #         data: dict = json.load(json_file)
    #     self.assertDictEqual(self.notionData.getProject(data['test_data']), data['expected_result'])

if __name__ == '__main__':
    unittest.main()
    