import json
import os
from styleframe import StyleFrame, Styler, utils
import pandas as pd
from tqdm import tqdm


PATH_OUTPUT_REPORT: str = r'./report_excel.xlsx'
REPORT_HEADER: dict = {
    'Task': 80.0,
    'Start Date': 15.0,
    'End Date': 15.0,
    'Total Work Hours': 25.0,
    'Project': 30.0,
}
DEFAULT_ROW_HEIGHT: int = 16  ## For font calibri 13


class GenerateExcel:
    def __init__(self):
        self.path_output_report: str = PATH_OUTPUT_REPORT

    def get_dict_data_from_jsonfile(self, path: str) -> dict:
        data_from_json_file: dict = {}
        _, file_extension = os.path.splitext(path)
        if file_extension.lower() != '.json':
            raise ValueError("File does not have a JSON extension.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")

        with open(path, 'r', encoding='utf-8') as file:
            data_from_json_file = json.load(file)
        return data_from_json_file

    def new_write_excel(self, data: dict):
        excel_writer = StyleFrame.ExcelWriter(self.path_output_report)
        for project in tqdm(data, ncols=100):
            dataframe_list: list = []
            persons_in_project: list = data[project]
            all_row: int = 0
            person_index_row: list = []
            summary_index_row: list = []
            for person in persons_in_project:
                # person
                person_row: list = [person, '', '', '', '']
                dataframe_list.append(person_row)
                person_index_row.append(all_row)
                all_row += 1
                tasks_of_person: list = data[project][person]
                total_man_hour: int = 0
                for task in tasks_of_person:
                    # task
                    details_task_row: list = [
                        task['title'],
                        task['start_date'],
                        task['end_date'],
                        task['total_work_hours'],
                        ', '.join(task['project'])
                    ]
                    total_man_hour += task['total_work_hours']
                    dataframe_list.append(details_task_row)
                    all_row += 1

                summary_row: list = ['Total Man-Hours', '', '',
                                     total_man_hour, '']
                dataframe_list.append(summary_row)
                summary_index_row.append(all_row)
                all_row += 1
                summary_man_days: list = ['Total Man-Hours / 8', '', '',
                                          total_man_hour/8, '']
                dataframe_list.append(summary_man_days)
                summary_index_row.append(all_row)
                all_row += 1

            # header
            headers_row: list = list(REPORT_HEADER.keys())
            dataframe = pd.DataFrame(dataframe_list, columns=headers_row)

            # style
            default_style = self.set_default_excel_style()
            style_frame = StyleFrame(dataframe, default_style)
            self.set_header_excel_style(style_frame)
            self.set_column_excel_style(style_frame)
            self.set_person_row_excel_style(style_frame, person_index_row)
            self.set_summary_row_excel_style(style_frame, summary_index_row)

            # size (width, height)
            self.set_column_excel_width(style_frame)
            self.set_row_excel_height(style_frame, all_row)
            style_frame.to_excel(excel_writer, sheet_name=project,
                columns_and_rows_to_freeze='A2')
        excel_writer.save()

    @staticmethod
    def set_default_excel_style():
        light_cyan_color: str = 'b7e1cd'
        default_style = Styler(
            horizontal_alignment='center',
            vertical_alignment='top',
            bg_color=light_cyan_color,
            font=utils.fonts.calibri,
            font_size=13
            )
        return default_style

    @staticmethod
    def set_header_excel_style(style_frame):
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

    @staticmethod
    def set_column_excel_style(style_frame):
        light_cyan_color: str = 'b7e1cd'
        ## Add column style follow header
        header_list: list = ['Task']
        column_style = Styler(
            horizontal_alignment='left',
            vertical_alignment='top',
            bg_color=light_cyan_color,
            font=utils.fonts.calibri,
            font_size=13
            )
        style_frame.apply_column_style(cols_to_style=header_list, styler_obj=column_style)

    @staticmethod
    def set_person_row_excel_style(style_frame, person_row: list):
        cyan_color: str = 'ff9898'
        person_row_style = Styler(
            horizontal_alignment='left',
            bg_color=cyan_color,
            bold=True,
            font=utils.fonts.calibri,
            font_size=15
        )
        for index_row in person_row:
            style_frame.apply_style_by_indexes(indexes_to_style=[index_row],
                                               styler_obj=person_row_style)

    @staticmethod
    def set_summary_row_excel_style(style_frame, summary_row: list):
        cyan_color: str = '46bdc6'
        last_row_style = Styler(
            bg_color=cyan_color,
            font_color=utils.colors.white,
            bold=True,
            font=utils.fonts.calibri,
            font_size=13
            )
        for index_row in summary_row:
            style_frame.apply_style_by_indexes(indexes_to_style=[index_row],
                                               styler_obj=last_row_style)

    @staticmethod
    def set_column_excel_width(style_frame):
        column_header_set: list = list(REPORT_HEADER.keys())
        for header in column_header_set:
            style_frame.set_column_width(columns=[header], width=REPORT_HEADER[header])

    @staticmethod
    def set_row_excel_height(style_frame, all_row: int):
        # first row (content data)
        row: int = 2
        for _ in range(all_row):
            style_frame.set_row_height(rows=[row], height=DEFAULT_ROW_HEIGHT)
            row += 1


if __name__=='__main__':
    generater = GenerateExcel()
    dict_data = generater.get_dict_data_from_jsonfile('./export_data.json')
    generater.new_write_excel(dict_data)
