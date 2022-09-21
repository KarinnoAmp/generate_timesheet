from dotmap import DotMap
from tqdm import tqdm
import requests
import yaml
import json
import time

notion_url = 'https://api.notion.com/v1/databases/e98588084035474394b5bec1651c6eef/query'
config     = DotMap(yaml.full_load(open('config.yaml', encoding='utf-8')))
json_data  = DotMap(json.load(open('json_object', encoding='utf-8')))

def set_header(notion_version):
    header = {
        'Authorization': 'Bearer secret_ftVfm6G44cEujeMsnIuxhSGeDV7IMSpZFHiu0YrjLrM',
        'Content Type': 'application/json',
        'Notion-Version': notion_version
    }
    return header

def set_body(start_date, end_date, person_key):
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
    # print(body)
    return body

# sending the request for get time sheet data
def send_request(url ,headers ,json_data):
    response = requests.post(url=url, headers=headers, json=json_data)
    # json_object = json.dumps(response.json(), indent=4)
    # with open("response_data", "w") as outfile:
    #     outfile.write(json_object)
    return DotMap(response.json())

# get list of tasks in notion
def get_tasks_content(json, person_name):
    content = list()
    print('\n' + person_name)
    for i in tqdm(range(len(json.results))):
    # Check task title
        if len(json.results[i].properties.Task.title) == 0:
            title = None
        else:
            title =  str(json.results[i].properties.Task.title[0].plain_text)            
    # Check tasks Status
        if json.results[i].properties.Status.status != None:
            status = json.results[i].properties.Status.status.name
        else:
            status = None
    # Check tasks Project
        if len(json.results[i].properties.Project.multi_select) > 1:
            project = ''
            for x in range(len(json.results[i].properties.Project.multi_select)):
                if x == 0:
                    project = str(json.results[i].properties.Project.multi_select[x].name)
                else:
                    project = str(project) + ', ' + str(json.results[i].properties.Project.multi_select[x].name)
        elif 1 >= len(json.results[i].properties.Project.multi_select) > 0:
            project = str(json.results[i].properties.Project.multi_select[0].name)
        else:
            project = None
        dict = {
            'title': title,
            'start_date': list(str(json.results[i].properties.Date.date.start).split('T', 1))[0],
            'end_date': list(str(json.results[i].properties.Date.date.end).split('T', 1))[0],
            'total_work_hours': json.results[i].properties['Work hours per person'].formula.number,
            'status': status,
            'project': project
        }
        content.append(dict)
        time.sleep(0.001)
    data = {
        'person': person_name,
        'data': content,
        'total': len(json.results)
    }
    return DotMap(data)

# get all time sheet data from person in config file
def generate_time_sheet_json_data(start_date, end_date):
    list = []
    for person_name in tqdm(config.persons.keys()):
        json_response = send_request(url=config.url, headers=set_header(str(config.notion_version)), json_data=set_body(start_date, end_date, str(config.persons[person_name])))
        # json_response = DotMap(json.load(open('response_data', encoding='UTF-8')))
        time_sheet_data = get_tasks_content(json_response, person_name)
        list.append(time_sheet_data)
    time_record = {
        'items': list
    }
    json_object = json.dumps(time_record, indent=4)
    with open("export_data_test", "w") as outfile:
        outfile.write(json_object)
    return time_record


# Writing to sample.json
x = generate_time_sheet_json_data(config.start_date, config.end_date)
json_object = json.dumps(x, indent=4)
with open("export_data", "w") as outfile:
    outfile.write(json_object)
    