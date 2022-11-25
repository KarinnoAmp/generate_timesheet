from dotmap import DotMap
from tqdm import tqdm
from txt_style import bcolors
import json
# from datetime import datetime
import requests
import yaml




config = DotMap(yaml.full_load(open('config.yaml', encoding='utf-8')))
text = bcolors()




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
    


    def setHeader(self, notion_version: str) -> object:
        '''Set request header'''
        header = {
            'Authorization': 'Bearer ' + str(config.authorization),
            'Content-Type': 'application/json',
            'Notion-Version': notion_version
        }
        return header



    def setBody(self, start_date: str, end_date: str, person_key: str, last_page=None) -> object:
        '''Set request body'''
        body = {
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



    def sendRequest(self, url: str ,headers: object ,json_data: object) -> object:
        '''sending the request for get time sheet data'''
        response = requests.post(url=url, headers=headers, json=json_data)
        if int(response.status_code) != 200:
            print(text.FAIL + (str('\n') * 2) + 'HTTP error status ' + str(response.status_code)) # Red color
            print('message: ' + str(response.json()['code']) + text.ENDC) # Red color
            exit()
        return DotMap(response.json())




class notionData:
    def __init__(self):
        self.request = setApi()
        self.math = mathCalculator()
        

    
    def summaryTasks(self, json: object, person_name: str) -> object:
        '''get list of tasks in notion'''
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
                    for x in range(len(json[y].results[i].properties.Project.multi_select)):
                        if x < 1:
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
                
        total_work_hours = self.math.roundNumber(total_work_hours, 2)
        timesheet_data = {
            'person': person_name,
            'data': content,
            'total_work_hours': total_work_hours
        }
        return DotMap(timesheet_data)
    
    

    def getTasksData(self, start_date:str, end_date:str) -> object:
        '''get all time sheet data from person in config file'''
        lst_timesheet_record = list()
        x = 0
        # print(text.BOLD + 'Generating timesheet from: ' + text.ENDC + text.WARNING + str(start_date.strftime('%d %b %Y')) + ' --> ' + str(end_date.strftime('%d %b %Y') + text.ENDC))
        for person_name in tqdm(config.persons.keys(), ncols=100, colour='cyan', desc='Loading data..'):
            i = 0
            boolean = True
            lst_response = list()
            while boolean == True:
            # First 100 Notion's tasks
                if i < 1:
                    data = self.request.setBody(str(start_date.date()), str(end_date.date()), str(config.persons[person_name]))
                    # data = self.request.setBody(str(start_date), str(end_date), str(config.persons[person_name]))
            # When Notion's tasks more than 100 tasks
                else:
                    data = self.request.setBody(str(start_date.date()), str(end_date.date()), str(config.persons[person_name]), str(json_response['next_cursor']))
                    # data = self.request.setBody(str(start_date), str(end_date), str(config.persons[person_name]))
                json_response = self.request.sendRequest(url=config.url, headers=self.request.setHeader(str(config.notion_version)), json_data=data)
                boolean = json_response['has_more']
                lst_response.append(json_response)
                i = i + 1
                # End of While
                
            time_sheet_data = self.summaryTasks(lst_response, person_name)
            lst_timesheet_record.append(time_sheet_data)
            x += 1
            # End of For
            
        timesheet_record = {
            'items': lst_timesheet_record
        }
        return timesheet_record




if __name__ == '__main__':
    timesheet_record = notionData().getTasksData('2022-10-01', '2022-10-31')
    json_object = json.dumps(timesheet_record, indent=4)
    with open("export_data.json", "w") as outfile:
        outfile.write(json_object)
