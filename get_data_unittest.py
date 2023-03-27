import unittest
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
    
    def test_setHeader(self):
        expect_result: dict = {
            'Authorization': 'Bearer secret_ftVfm6G44cEujeMsnIuxhSGeDV7IMSpZFHiu0YrjLrM',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.assertDictEqual(self.setApi.setHeader(), expect_result)
    
    def test_setBody(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        expect_result: dict = {
            'filter': {
                'and': [
                    {
                        'property': 'Task type', 
                        'select': {
                            'does_not_equal': 'Information'
                        }
                    },
                    {
                        'property': 'Responsible person', 
                        'people': {
                            'contains': '6cb3cc27-680d-4026-a3e6-39681191582a'
                        }
                    }, 
                    {
                        'and': [
                            {
                                'property': 'Date', 
                                'date': {
                                    'on_or_before': '2022-11-11'
                                }
                            }, 
                            {
                                'property': 'Date', 
                                'date': {
                                    'on_or_after': '2022-11-11'
                                }
                            }
                        ]
                    }, 
                    {
                        'property': 'Tags', 
                        'multi_select': {
                            'does_not_contain': 'Leave'
                        }
                    }, 
                    {
                        'property': 'Tags', 
                        'multi_select': {
                            'does_not_contain': 'Holiday'
                        }
                    }, 
                    {
                        'property': 'Task type',
                        'select': {
                            'does_not_equal': 'Leave'
                        }
                    }, 
                    {
                        'property': 'Task type', 
                        'select': {
                            'does_not_equal': 'Information'
                        }
                    }
                ]
            }, 
            'sorts': [
                {
                    'property': 'Date', 
                    'direction': 'ascending'
                }
            ]
        }
        self.assertDictEqual(self.setApi.setBody(start_date, end_date, person_key), expect_result)
    
    def test_setBody_withMoreThan_100_items(self):
        start_date: str = '2022-11-11'
        end_date:   str = '2022-11-11'
        person_key: str = '6cb3cc27-680d-4026-a3e6-39681191582a'
        last_page:  str = 'Hello'
        expect_result: dict = {
            'filter': {
                'and': [
                    {
                        'property': 'Task type', 
                        'select': {
                            'does_not_equal': 'Information'
                        }
                    },
                    {
                        'property': 'Responsible person', 
                        'people': {
                            'contains': '6cb3cc27-680d-4026-a3e6-39681191582a'
                        }
                    }, 
                    {
                        'and': [
                            {
                                'property': 'Date', 
                                'date': {
                                    'on_or_before': '2022-11-11'
                                }
                            }, 
                            {
                                'property': 'Date', 
                                'date': {
                                    'on_or_after': '2022-11-11'
                                }
                            }
                        ]
                    }, 
                    {
                        'property': 'Tags', 
                        'multi_select': {
                            'does_not_contain': 'Leave'
                        }
                    }, 
                    {
                        'property': 'Tags', 
                        'multi_select': {
                            'does_not_contain': 'Holiday'
                        }
                    }, 
                    {
                        'property': 'Task type',
                        'select': {
                            'does_not_equal': 'Leave'
                        }
                    }, 
                    {
                        'property': 'Task type', 
                        'select': {
                            'does_not_equal': 'Information'
                        }
                    }
                ]
            }, 
            'sorts': [
                {
                    'property': 'Date', 
                    'direction': 'ascending'
                }
            ],
            'start_cursor': last_page
        }
        self.assertDictEqual(self.setApi.setBody(start_date, end_date, person_key, last_page), expect_result)
    
    def test_sendRequest(self):
        
    
if __name__ == '__main__':
    unittest.main()