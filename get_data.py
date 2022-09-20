from dotmap import DotMap
import requests

notion_url = 'https://api.notion.com/v1/databases/e98588084035474394b5bec1651c6eef/query'

def set_header():
    header = {
        'Authorization': 'Bearer secret_ftVfm6G44cEujeMsnIuxhSGeDV7IMSpZFHiu0YrjLrM',
        'Content Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    return DotMap(header)

def set_body(start_date, end_date, person):
    body = {
        'filter':{
            'and': [
                {
                    'property': 'Responsible person',
                    'people': {
                        'contains': str(person)
                    }
                },
                {
                    'and': [
                        {
                            'property': 'Date',
                            'date': {
                                'on_or_before': str(end_date)
                            }
                        },
                        {
                            'property': 'Date',
                            'date': {
                                'on_or_after': str(start_date)
                            }
                        }
                    ]
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
    return DotMap(body)

def send_request():
    x = requests.post(url=str(notion_url), headers=set_header(), json=set_body('2022-09-01', '2022-09-30', 'fb6ab337-1d37-4efc-8730-efbe2c602a9f'))
    return DotMap(x.json())

print(send_request())

# def get_data():
    