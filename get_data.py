import os
from dotmap import DotMap
from tqdm import tqdm
import numbers
import requests
import yaml
import json

notion_url = 'https://api.notion.com/v1/databases/e98588084035474394b5bec1651c6eef/query'
config     = DotMap(yaml.full_load(open('config.yaml', encoding='utf-8')))
os_name    = str(os.name)
# json_data  = DotMap(json.load(open('response_data', encoding='utf-8')))

def round_number(number: numbers, decimal: int=0):
    digit = int('1' + (str(0) * decimal))
    number = number * digit
    mod_number = number % 1
    if mod_number >= 0.5:
        round_number = (int(number) + 1)/digit
    else:
        round_number = (int(number)/digit)
    return round_number
    
def set_header(notion_version):
    header = {
        'Authorization': 'Bearer secret_ftVfm6G44cEujeMsnIuxhSGeDV7IMSpZFHiu0YrjLrM',
        'Content Type': 'application/json',
        'Notion-Version': notion_version
    }
    return header

def set_body(start_date, end_date, person_key: str, last_page=None):
    body = {
        'filter': {
            'and': [
                {
                    'property': 'Responsible person',
                    'people': {
                        'contains': str(person_key)
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
    if last_page != None:
        body.update({'start_cursor': str(last_page)})
    # print(body)
    return body

# sending the request for get time sheet data
def send_request(url: str ,headers: object ,json_data: object):
    response = requests.post(url=url, headers=headers, json=json_data)
    if int(response.status_code) != 200:
        print('\033[91m' + 'HTTP error status ' + str(response.status_code)) # Red color
        print('\033[91m' + str(response.json()['code'])) # Red color
        exit()
    # json_object = json.dumps(response.json(), indent=4)
    # with open("response_data.json", "w") as outfile:
    #     outfile.write(json_object)
    return DotMap(response.json())

# get list of tasks in notion
def get_tasks_content(json, person_name):
    content = list()
    total_work_hours = float(0)
    # print('\n' + person_name)
    for y in range(len(json)):
        for i in range(len(json[y].results)):
        # Check task title
            if len(json[y].results[i].properties.Task.title) == 0:
                title = None
            else:
                title =  str(json[y].results[i].properties.Task.title[0].plain_text)    
        # Check start date
            if json[y].results[i].properties.Date.date.start != None:
                start_date = list(str(json[y].results[i].properties.Date.date.start).split('T', 1))[0]
            else:
                start_date = None
        # Check end date
            if json[y].results[i].properties.Date.date.end != None:
                end_date = list(str(json[y].results[i].properties.Date.date.end).split('T', 1))[0]
            else:
                end_date = None
        # Set work hours
            work_hours = float(json[y].results[i].properties['Work hours per person'].formula.number)
        # Check tasks Status
            if json[y].results[i].properties.Status.status != None:
                status = json[y].results[i].properties.Status.status.name
            else:
                status = None
        # Check tasks Project
            if len(json[y].results[i].properties.Project.multi_select) > 1:
                project = ''
                for x in range(len(json[y].results[i].properties.Project.multi_select)):
                    if x == 0:
                        project = str(json[y].results[i].properties.Project.multi_select[x].name)
                    else:
                        project = str(project) + ', ' + str(json[y].results[i].properties.Project.multi_select[x].name)
            elif 1 >= len(json[y].results[i].properties.Project.multi_select) > 0:
                project = str(json[y].results[i].properties.Project.multi_select[0].name)
            else:
                project = None
        # Set data to dictionary
            dict = {
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'total_work_hours': work_hours,
                'status': status,
                'project': project
            }
            total_work_hours = total_work_hours + dict['total_work_hours']
            content.append(dict)
    total_work_hours = round_number(total_work_hours, 2)
    timesheet_data = {
        'person': person_name,
        'data': content,
        'total_work_hours': total_work_hours
    }
    return DotMap(timesheet_data)

# get all time sheet data from person in config file
def generate_time_sheet_json_data(start_date, end_date):
    lst_time_record = list()
    x = 0
    y = len(list(config.persons.keys()))
    for person_name in tqdm(config.persons.keys()):
        boo_lean = True
        i = 0
        lst_response = list()
        if y - x == 1:
            if str(os.name) == 'posix':
                os.system('clear')
            elif str(os.name) == 'nt':
                os.system('cls')
            print('\033[92m') # Green color
        while boo_lean == True:
            if i < 1:
                json_response = send_request(url=config.url, headers=set_header(str(config.notion_version)), json_data=set_body(start_date, end_date, str(config.persons[person_name])))
                # json_response = DotMap(json.load(open('response_data.json', encoding='UTF-8')))
            else:
                json_response = send_request(url=config.url, headers=set_header(str(config.notion_version)), json_data=set_body(start_date, end_date, str(config.persons[person_name]), str(json_response['next_cursor'])))
                # json_response = DotMap(json.load(open('response_data.json', encoding='UTF-8')))
            boo_lean = json_response['has_more']
            lst_response.append(json_response)
            i = i + 1
        time_sheet_data = get_tasks_content(lst_response, person_name)
        lst_time_record.append(time_sheet_data)
        x = x + 1
    time_record = {
        'items': lst_time_record
    }
    return time_record

# Writing to sample.json
x = generate_time_sheet_json_data(config.start_date, config.end_date)
json_object = json.dumps(x, indent=4)
with open("export_data.json", "w") as outfile:
    outfile.write(json_object)