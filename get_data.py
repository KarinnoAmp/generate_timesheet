from dotmap import DotMap
from tqdm import tqdm
from txt_style import bcolors as text
from datetime import datetime
import os
import json
import requests
import yaml



try:
    config: DotMap = DotMap(yaml.full_load(open(str('config.yaml'), encoding='utf-8')))
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
        pass
    


    def setHeader(self, notion_version: str) -> dict:
        '''Set request header'''
        header: dict = {
            'Authorization': 'Bearer ' + str(config.authorization),
            'Content-Type': 'application/json',
            'Notion-Version': notion_version
        }
        # print(header)
        return header



    def setBody(self, start_date: str, end_date: str, person_key: str, last_page=None) -> dict:
        '''Set request body'''
        body: dict= {
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
        if last_page != None:
            body.update({'start_cursor': str(last_page)})
        # print(body)
        return body



    def sendRequest(self, url: str ,headers: dict ,json_data: json) -> DotMap:
        '''sending the request for get time sheet data'''
        response = requests.post(url=url, headers=headers, json=json_data)
        if int(response.status_code) != 200:
            self.clear
            print(text.FAIL + (str('\n') * 2) + 'HTTP error status ' + str(response.status_code)) # Red color
            print('message: ' + str(response.json()['code']) + text.ENDC) # Red color
            exit()
        return DotMap(response.json())



    def setBodyGetPerson(self) -> dict:
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
        # print(body)
        return  body



class notionData:
    def __init__(self):
        self.request = setApi()
        self.math = mathCalculator()
        

    
    def summaryTasks(self, lst_response: list and DotMap, person_name: str) -> dict:
        '''get list of tasks in notion'''
        content: list = list()
        total_work_hours: float = float(0)
        # 2 loops when have more than 100 data
        for y in range(len(lst_response)):
            # Getting all result data and setting format
            for i in range(len(lst_response[y].results)):
            # Get task title
                if len(lst_response[y].results[i].properties.Task.title) == 0:
                    title = None
                else:
                    title: str =  str(lst_response[y].results[i].properties.Task.title[0].plain_text)   
                     
            # Get start date
                if lst_response[y].results[i].properties.Date.date.start != None:
                    start_date: datetime = datetime.strptime(list(str(lst_response[y].results[i].properties.Date.date.start).split('T', 1))[0], '%Y-%m-%d')
                    start_date: str = str(start_date.strftime('%d/%m/%Y'))
                else:
                    start_date = None
            
            # Get end date
                if lst_response[y].results[i].properties.Date.date.end != None:
                    end_date: datetime = datetime.strptime(list(str(lst_response[y].results[i].properties.Date.date.start).split('T', 1))[0], '%Y-%m-%d')
                    end_date: str = str(end_date.strftime('%d/%m/%Y'))
                    # end_date: str = list(str(lst_response[y].results[i].properties.Date.date.end).split('T', 1))[0]
                else:
                    end_date = None
            
            # Get work hours
                work_hours: float = float(lst_response[y].results[i].properties['Work hours per person'].formula.number)
            
            # Get tasks Status
                if lst_response[y].results[i].properties.Status.status != None:
                    status: str = lst_response[y].results[i].properties.Status.status.name
                else:
                    status = None
            
            # Get tasks Project
                if len(lst_response[y].results[i].properties.Project.multi_select) > 1: # have more than 1 project
                    for x in range(len(lst_response[y].results[i].properties.Project.multi_select)):
                        if x < 1:
                            project: str = str(lst_response[y].results[i].properties.Project.multi_select[x].name)
                        else:
                            project: str = str(project) + ', ' + str(lst_response[y].results[i].properties.Project.multi_select[x].name)
                elif 1 >= len(lst_response[y].results[i].properties.Project.multi_select) > 0: # have 1 project
                    project: str = str(lst_response[y].results[i].properties.Project.multi_select[0].name)
                else: # don't contain any project
                    project = None
            
            # Set data to dictionary
                task_dict = {
                    'title': title,
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_work_hours': work_hours,
                    'status': status,
                    'project': project
                }
                
                total_work_hours: float = total_work_hours + task_dict['total_work_hours']
                content.append(task_dict)
                
        total_work_hours: float = self.math.roundNumber(total_work_hours, 2)
        timesheet_data: dict = {
            'person': person_name,
            'data': content,
            'total_work_hours': total_work_hours
        }
        return timesheet_data
    
    

    def getTasksData(self, start_date: datetime, end_date: datetime) -> dict:
        '''get all time sheet data from person in config file'''
        lst_timesheet_record: list = list()
        x = 0
        persons: dict = self.getPerson()
        # Getting all person tasks
        for person_name in tqdm(persons.keys(), ncols=100, colour='cyan', desc='Requesting data..'):
            i = 0
            lst_response: list= list()
            # Getting all tasks of person
            while True:
                # First 100 Notion's tasks
                if i < 1:
                    data: dict = self.request.setBody(str(start_date.date()), str(end_date.date()), str(persons[person_name]))
                # Another 100 Notion's tasks
                else:
                    data: dict = self.request.setBody(str(start_date.date()), str(end_date.date()), str(persons[person_name]), str(json_response['next_cursor']))
                json_response: DotMap = self.request.sendRequest(url=config.url, headers=self.request.setHeader(str(config.notion_version)), json_data=data)
                lst_response.append(json_response)
                if not json_response['has_more']: # When do not have more 100 tasks left
                    break
                else:
                    i += 1
                
            time_sheet_data: object = self.summaryTasks(lst_response, person_name)
            lst_timesheet_record.append(time_sheet_data)
            x += 1
            
        timesheet_record: dict = {
            'items': lst_timesheet_record
        }
        return timesheet_record



    def getPerson(self) -> dict:
        data: dict = self.request.setBodyGetPerson()
        json_response = self.request.sendRequest(url=config.url, headers=self.request.setHeader(str(config.notion_version)), json_data=data)
        persons: dict = dict()
        for person_data in tqdm(json_response.results[0].properties['Responsible person'].people, ncols=100, colour='cyan', desc='Getting person..'):
            persons.update({person_data['name']: person_data['id']})
        # print(persons)
        return persons





if __name__ == '__main__':
    start_date: str= '01-11-2022'
    end_date: str = '01-11-2022'
    timesheet_record: dict = notionData().getTasksData(datetime.strptime(str(start_date), '%d-%m-%Y'), datetime.strptime(str(end_date), '%d-%m-%Y'))
    json_object: dict = json.dumps(timesheet_record, indent=4)
    with open("export_data.json", "w") as outfile:
        outfile.write(json_object)
    # notionData().getPerson()