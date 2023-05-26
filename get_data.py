from tqdm import tqdm
from txt_style import bcolors
from datetime import datetime
import json, os
import requests
import yaml

text = bcolors()
try:
    config_path: str = str(os.path.join(os.getcwd(), 'config.yaml'))
    print(config_path)
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
        self.ALL_PROJECT = dict()
    
    def setBody(self, start_date: str, end_date: str, last_page: str=None) -> dict:
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

    def sendRequestGetPerson(self) -> dict:
        self.setBodyGetPerson()
        json_response: dict = self.sendRequest()
        return json_response

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
        self.ALL_PROJECT = dict()
    
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
    
    def checkTaskProject(self, project_list: list) -> str:
        projects = list()
        if len(project_list) > 0:
            for project in project_list:
                projects.append(project['name'])
        else:
            projects = None
        return projects
    
    def summaryTasks(self, json_data: list) -> object:
        '''get list of tasks in notion'''
        for task in json_data:
            if not task['project']:
                continue
            else:
                for project in task['project']:
                    for person_name in task['responsible_person']:
                        if project not in list(self.ALL_PROJECT.keys()):
                            self.ALL_PROJECT[project] = dict()
                        try:
                            name = person_name['name']
                        except KeyError:
                            name = 'no_name'
                        if name not in list(self.ALL_PROJECT[project].keys()):
                            self.ALL_PROJECT[project][name] = list()
                        self.ALL_PROJECT[project][name].append(
                            {
                                'title': task['title'],
                                'start_date': task['start_date'],
                                'end_date': task['end_date'],
                                'total_work_hours': task['total_work_hours'],
                                'project': task['project']
                            }
                        )
        return self.ALL_PROJECT
    
    def formattedTasks(self, json_data: list) -> object:
        list_projects: list = list()
        for tasks in json_data:
            if not tasks['results']:
                continue
            else:
                for task in tasks['results']:
                    # Set data to dictionary
                    task_dict = {
                        'title': self.checkTaskTitle(task['properties']['Task']['title']),
                        'start_date': self.checkDateFormat(task['properties']['Date']['date']['start']),
                        'end_date': self.checkDateFormat(task['properties']['Date']['date']['end']),
                        'total_work_hours': float(task['properties']['Work hours per person']['formula']['number']),
                        'status': task['properties']['Status']['status']['name'],
                        'responsible_person': task['properties']['Responsible person']['people'],
                        'project': self.checkTaskProject(task['properties']['Project']['multi_select'])
                    }
                    list_projects.append(task_dict)
        return list_projects
    
    def getAllTasksData(self, start_date: datetime, end_date: datetime) -> dict:
        '''get all time sheet data from person in config file'''
        lst_personal_task: list = self.getTaskData(start_date, end_date) # non-format data
        lst_personal_task = self.formattedTasks(lst_personal_task)
        self.summaryTasks(lst_personal_task)
        return self.ALL_PROJECT
    
    def getTaskData(self, start_date: datetime, end_date: datetime) -> list:
        lst_personal_task: list = list() # All tasks of 1 person non-format
        personal_tasks: dict = dict({'next_cursor': None})
        while True:
            '''Collect all task of person'''
            self.request.setBody(
                str(start_date.date()),
                str(end_date.date()),
                personal_tasks['next_cursor']
            )
            personal_tasks: dict = self.request.sendRequest()
            lst_personal_task.append(personal_tasks)
            if not personal_tasks['has_more']: # Will do this when has no more that 100 tasks in 1 requests
                break
        with open('export.json', 'w') as json_file:
            json.dump(lst_personal_task, json_file, indent=4)
        return lst_personal_task
    
    # def getPerson(self, response: dict) -> dict:
    #     persons = dict()
    #     for data in tqdm(
    #         response['results'][0]['properties']['Responsible person']['people'], 
    #         ncols=100, colour='cyan', desc='Getting person..'
    #     ):
    #         persons[data['name']] = data['id']
    #     return persons
    
    # def getProject(self, dict_data: dict) -> list:
    #     project_dict = dict()
    #     for project in dict_data['results'][0]['properties']['Project']['multi_select']:
    #         project_dict[project['name']] = dict()
    #     self.ALL_PROJECT = project_dict
    #     return project_dict

if __name__ == '__main__':
    # start_date: str= '01-12-2022'
    # end_date: str = '31-12-2022'
    # timesheet_record: dict = notionData().getAllTasksData(datetime.strptime(str(start_date), '%d-%m-%Y'), datetime.strptime(str(end_date), '%d-%m-%Y'))
    # with open("export_data.json", "w") as json_outfile:
    #     json.dump(timesheet_record, json_outfile, indent=4)
    with open("response.json", "r") as json_infile:
        json_data: list = json.load(json_infile)
    list_data = notionData().formattedTasks(json_data)
    with open("formatted_tasks.json", "w") as json_outfile:
        json.dump(list_data, json_outfile, indent=4)
    summary_data = notionData().summaryTasks(list_data)
    with open("summary_data.json", "w") as json_outfile:
        json.dump(summary_data, json_outfile, indent=4)
    