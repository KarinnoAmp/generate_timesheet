import json
from styleframe import StyleFrame, Styler, utils
import pandas as pd
from tqdm import tqdm


PATH_OUTPUT_REPORT: str = r'./report_excel.xlsx'
REPORT_HEADER: dict = {
    'Title': 80.0,
    'Start Date': 15.0,
    'End Date': 15.0,
    'Total Work Hours': 25.0,
    'Status': 15.0,
    'Project': 15.0,
}
DEFAULT_ROW_HEIGHT: int = 13  ## For font calibri 13


class GenerateExcel:
    def __init__(self):
        self.path_output_report: str = PATH_OUTPUT_REPORT

    def get_dict_data_from_jsonfile(self, path: str) -> dict:
        data_from_json_file: dict = {}
        with open(path, 'r', encoding='utf-8') as file:
            data_from_json_file = json.load(file)
        return data_from_json_file

    def write_excel(self, data: dict):
        excel_writer = StyleFrame.ExcelWriter(PATH_OUTPUT_REPORT)
        for item in tqdm(data['items']):
            person_name: str = item['person']
            person_task: list = item['data']
            headers: list = list(REPORT_HEADER.keys())
            dataframe_list: list = []
            all_task: int = len(person_task)
            for task in person_task:
                detail: list = [
                    task['title'],
                    task['start_date'],
                    task['end_date'],
                    task['total_work_hours'],
                    task['status'],
                    task['project']
                    ]
                dataframe_list.append(detail)
            last_row_data: int = all_task + 1
            summary_row: list = ['Total Man-Hours', '', '',
                f'=SUBTOTAL(9, D2:D{last_row_data})', '', '']
            summary_row_data: int = last_row_data + 1
            summary_man_days: list = ['Total Man-Hours / 8', '', '',
                f'=D{summary_row_data}/8', '', '']
            dataframe_list.append(summary_row)
            dataframe_list.append(summary_man_days)
            dataframe = pd.DataFrame(dataframe_list, columns=headers)
            default_style = self.set_default_excel_style()
            style_frame = StyleFrame(dataframe, styler_obj=default_style)
            self.set_header_excel_style(style_frame)
            self.set_column_excel_style(style_frame)
            self.set_last_row_excel_style(style_frame, all_task)
            self.set_column_excel_width(style_frame)
            style_frame.to_excel(excel_writer, sheet_name=person_name,
                row_to_add_filters=0,
                columns_and_rows_to_freeze='A2')
        excel_writer.save()

    ## New Function Implement
    def write_new_excel_style(self, data: dict):
        excel_writer = StyleFrame.ExcelWriter(PATH_OUTPUT_REPORT)
        for item in tqdm(data['items']):
            person_name: str = item['person']
            person_task: list = item['data']
            person_total_work_hours: str = item['total_work_hours']
            headers: list = list(REPORT_HEADER.keys())
            dataframe: list = []
            ## Initial data
            previous_date: str = ''
            task_end_date: str = ''
            title_list: list = []
            project_list: list = []
            total_work_hours_per_date: int = 0
            height_point_style: list = []
            number_all_task: int = len(person_task)
            for index, task in enumerate(person_task):
                if index != 0 and \
                    (task['start_date'] != previous_date or number_all_task == index + 1):
                    ## Add data to dataframe
                    all_task_per_date: str = '\n'.join(title_list)
                    number_all_task_per_date = len(title_list)
                    height_point: int = number_all_task_per_date * DEFAULT_ROW_HEIGHT
                    height_point_style.append(height_point)
                    if task_end_date < task['start_date']:
                        task_end_date = task['start_date']
                    detail: list = [
                        all_task_per_date,
                        task['start_date'],
                        task_end_date,
                        total_work_hours_per_date,
                        task['status'],
                        project_list
                        ]
                    dataframe.append(detail)
                    title_list = []
                    total_work_hours_per_date = 0
                    task_end_date = ''
                ## Add title
                task_title: str = task['title']
                if task_title is None:
                    title_list.append('')
                else:
                    title_list.append(f"- {task_title}")
                ## Add project
                project_name: str = task['project']
                if task_title is None:
                    project_list.append('')
                else:
                    project_list.append(project_name)
                ## Check group date
                previous_date = task['start_date']
                ## Add end date
                end_date: str = task['end_date']
                if end_date != '' and end_date is not None:
                    task_end_date = end_date
                ## Summary work hours
                total_work_hour: int = int(task['total_work_hours'])
                total_work_hours_per_date += total_work_hour

            summary_man_hours: list = ['Total Man-Hours', '', '',
                person_total_work_hours, '', '']
            summary_man_days: list = ['Total Man-Hours / 8', '', '',
                person_total_work_hours / 8, '', '']
            dataframe.append(summary_man_hours)
            dataframe.append(summary_man_days)
            df = pd.DataFrame(dataframe, columns=headers)
            default_style = self.set_default_excel_style()
            sf = StyleFrame(df, styler_obj=default_style)
            self.set_header_excel_style(sf)
            self.set_column_excel_style(sf)
            self.set_last_row_excel_style(sf, number_all_task)
            self.set_column_excel_width(sf)
            self.set_row_excel_height(sf, height_point_style)
            sf.to_excel(excel_writer, sheet_name=person_name, columns_and_rows_to_freeze='A2')
        excel_writer.save()

    def set_default_excel_style(self):
        light_cyan_color: str = 'b7e1cd'
        default_style = Styler(
            horizontal_alignment='center',
            vertical_alignment='top',
            bg_color=light_cyan_color,
            font=utils.fonts.calibri,
            font_size=13
            )
        return default_style

    def set_header_excel_style(self, style_frame):
        cyan_color: str = '46bdc6'
        header_style = Styler(
            horizontal_alignment='center',
            vertical_alignment='center',
            bg_color=cyan_color,
            font_color=utils.colors.white,
            bold=True,
            font=utils.fonts.calibri,
            font_size=15
            )
        style_frame.apply_headers_style(styler_obj=header_style)

    def set_column_excel_style(self, style_frame):
        light_cyan_color: str = 'b7e1cd'
        ## Add column style follow header
        header_list: list = ['Title']
        column_style = Styler(
            horizontal_alignment='left',
            vertical_alignment='top',
            bg_color=light_cyan_color,
            font=utils.fonts.calibri,
            font_size=13
            )
        style_frame.apply_column_style(cols_to_style=header_list, styler_obj=column_style)

    def set_last_row_excel_style(self, style_frame, last_row_data: int):
        cyan_color: str = '46bdc6'
        last_row_style = Styler(
            bg_color=cyan_color,
            font_color=utils.colors.white,
            bold=True,
            font=utils.fonts.calibri,
            font_size=15
            )
        text_summary_last_row_style = Styler(
            horizontal_alignment='right',
            vertical_alignment='top',
            bg_color=cyan_color,
            font_color=utils.colors.white,
            bold=True,
            font=utils.fonts.calibri,
            font_size=15
            )
        for _ in range(2):
            style_frame.apply_style_by_indexes(indexes_to_style=[last_row_data],
                styler_obj=last_row_style)
            style_frame.apply_style_by_indexes(indexes_to_style=[last_row_data],
                cols_to_style=['Title'],
                styler_obj=text_summary_last_row_style
                )
            last_row_data += 1

    def set_column_excel_width(self, style_frame):
        column_header_set: list = list(REPORT_HEADER.keys())
        for header in column_header_set:
            style_frame.set_column_width(columns=[header], width=REPORT_HEADER[header])

    def set_row_excel_height(self, style_frame, height_point_style: list):
        last_row: int = len(height_point_style)
        row: int = 2
        for index_row in range(last_row):
            style_frame.set_row_height(rows=[row], height=height_point_style[index_row])
            row += 1


## For Test
generator = GenerateExcel()
dict_data = generator.get_dict_data_from_jsonfile('./export_data.json')
generator.write_excel(dict_data)
# generator.write_new_excel_style(dict_data)
