from tqdm import tqdm
from txt_style import bcolors
from datetime import datetime
import json, os
import requests
import yaml

text = bcolors()
try:
    config_path: str = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))
    config = yaml.full_load(open(config_path, encoding='utf-8'))
except FileNotFoundError:
    print(text.FAIL + 'Cannot find config.yaml file' + text.ENDC)
    input('Press Enter to continue..')
    exit()

class mathCalculator:
    def __init__(self) -> None:
        pass
    
    def roundNumber(self, number: float, decimal: int=0) -> float:
        '''Round the decimal in number'''
        digit = int('1' + (str(0) * decimal))
        number = number * digit
        mod_number = number % 1
        if mod_number >= 0.5:
            round_number = (int(number) + 1)/digit
        else:
            round_number = (int(number)/digit)
        return round_number

class setApi:
    def __init__(self) -> None:
        self.HEADER = {
            'Authorization': 'Bearer ' + str(config['authorization']),
            'Content-Type': 'application/json',
            'Notion-Version': str(config['notion_version'])
        }
        self.BODY = None
        self.URL = config['url']

    def setBody(self, start_date: str, end_date: str, person_key: str, last_page: str=None) -> dict:
        '''Set request body'''
        body: dict = {
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
                            'contains': person_key
                        }
                    },
                    {
                        'and': [
                            {
                                'property': 'Date',
                                'date': {
                                    'on_or_before': end_date
                                }
                            },
                            {
                                'property': 'Date',
                                'date': {
                                    'on_or_after': start_date
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
        if last_page:
            body.update({'start_cursor': str(last_page)})
        self.BODY = body
        return body

    def sendRequest(self, url=None, headers=None, json_data=None) -> json:
        '''sending the request for get time sheet data'''
        url = url or self.URL
        headers = headers or self.HEADER
        json_data = json_data or self.BODY
        response = requests.post(url=url, headers=headers, json=json_data)
        if int(response.status_code) != 200:
            raise(ConnectionError(str(response.status_code) + '\n' + 'message: ' + str(response.json())))
        return response.json()

    def setBodyGetPerson(self, start_date: str = '2022-11-01', end_date: str = '2022-11-01') -> dict:
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise ValueError('start_date or end_date was in wrong type')
        body: dict = {
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
                            'on_or_before': end_date
                        }
                    },
                    {
                        'property': 'Date',
                        'date': {
                            'on_or_after': start_date
                        }
                    }
                ]
            }
        }
        self.BODY = body
        return  body

class notionData:
    def __init__(self):
        self.request = setApi()
        self.math = mathCalculator()
    
    def checkTaskTitle(self, task_title: list) -> str:
        if not task_title:
            return None
        else:
            return str(task_title[0]['plain_text'])
    
    def checkDateFormat(self, date: str) -> str:
        '''Check if date exists and format it to '%d/%m/%Y'.'''
        if date and date != 'None':
            date_formatted = datetime.strptime(date.split('T', 1)[0], '%Y-%m-%d')
            date_formatted = str(date_formatted.strftime('%d/%m/%Y'))
        else:
            date_formatted = None
        return date_formatted
    
    def checkTaskProject(self, project_list: list):
        if len(project_list) > 1:
            for x in range(len(project_list)):
                if x < 1:
                    project: str = str(project_list[x]['name'])
                else:
                    project: str = str(project) + ', ' + str(project_list[x]['name'])
        elif 1 >= len(project_list) > 0:
            project: str = str(project_list[0]['name'])
        else:
            project = None
        return project
    
    def summaryTasks(self, json_data: list, person_name: str) -> object:
        '''get list of tasks in notion'''
        content = list()
        total_work_hours = float(0)
        for data in json_data:
            if not data['results']:
                break
            for result in data['results']:
                # Set data to dictionary
                dict = {
                    'title': self.checkTaskTitle(result['properties']['Task']['title']),
                    'start_date': self.checkDateFormat(result['properties']['Date']['date']['start']),
                    'end_date': self.checkDateFormat(result['properties']['Date']['date']['end']),
                    'total_work_hours': float(result['properties']['Work hours per person']['formula']['number']),
                    'status': result['properties']['Status']['status']['name'],
                    'project': self.checkTaskProject(result['properties']['Project']['multi_select'])
                }
                total_work_hours = total_work_hours + dict['total_work_hours']
                content.append(dict)
        total_work_hours: float = self.math.roundNumber(total_work_hours, 2)
        timesheet_data: dict = {
            'person': person_name,
            'data': content,
            'total_work_hours': total_work_hours
        }
        return timesheet_data

    def getAllTasksData(self, start_date: datetime, end_date: datetime) -> dict:
        '''get all time sheet data from person in config file'''
        lst_timesheet_record: list = list() # All tasks of all person with format
        persons: dict = self.getPerson()
        for person_name in tqdm(persons.keys(), ncols=100, colour='cyan', desc='Requesting data..'):
            '''Collect all person tasks'''
            lst_personal_task: list = self.getTaskData(start_date, end_date, personal_id=persons[person_name]) # non-format data
            formatted_data: object = self.summaryTasks(lst_personal_task, person_name)
            lst_timesheet_record.append(formatted_data)
        timesheet_record: dict = {
            'items': lst_timesheet_record
        }
        return timesheet_record
    
    def getTaskData(self, start_date: datetime, end_date: datetime, personal_id: str) -> dict:
        lst_personal_task: list = list() # All tasks of 1 person non-format
        personal_tasks: dict = dict({'next_cursor': None})
        while True:
            '''Collect all task of person'''
            self.request.setBody(
                str(start_date.date()),
                str(end_date.date()),
                str(personal_id),
                personal_tasks['next_cursor']
            )
            personal_tasks: dict = self.request.sendRequest()
            lst_personal_task.append(personal_tasks)
            if not personal_tasks['has_more']: # Will do this when has no more that 100 tasks in 1 requests
                break
        return lst_personal_task

    def getPerson(self) -> dict:
        data = self.request.setBodyGetPerson()
        json_response = self.request.sendRequest()
        persons = dict()
        for data in tqdm(
            json_response['results'][0]['properties']['Responsible person']['people'], 
            ncols=100, colour='cyan', desc='Getting person..'
        ):
            persons.update({data['name']: data['id']})
        return persons

if __name__ == '__main__':
    start_date: str= '03-05-2023'
    end_date: str = '03-05-2023'
    timesheet_record: dict = notionData().getAllTasksData(datetime.strptime(str(start_date), '%d-%m-%Y'), datetime.strptime(str(end_date), '%d-%m-%Y'))
    json_object: dict = json.dumps(timesheet_record, indent=4)
    with open("export_data.json", "w") as outfile:
        outfile.write(json_object)
    # print(notionData().getPerson())
    