import json
from styleframe import StyleFrame, Styler, utils
import pandas as pd
from tqdm import tqdm


PATH_OUTPUT_REPORT: str = r'./report_excel.xlsx'
REPORT_HEADER: dict = {
    'Title': 50.0,
    'Start Date': 25.0,
    'End Date': 25.0,
    'Total Work Hours': 25.0,
    'Status': 25.0,
    'Project': 25.0,
}


class GenerateExcel:
    def __init__(self):
        self.path_output_report: str = PATH_OUTPUT_REPORT
    
    
    def get_dict_data_from_jsonfile(self, path: str) -> dict:
        dict_data: dict = {}
        with open(path, 'r') as file:
            dict_data = json.load(file)
        return dict_data
    
    
    def write_excel(self, data: dict):
        # workbook = load_workbook(self.path_output_report)
        excel_writer = StyleFrame.ExcelWriter(PATH_OUTPUT_REPORT)
        
        for item in tqdm(data['items']):
            person_name: str = item['person']
            person_task: list = item['data']
            person_total_work_hours: str = item['total_work_hours']
            
            headers: list = list(REPORT_HEADER.keys())
            dataframe: list = []
            for task in person_task:
                detail: list = [
                    task['title'],
                    task['start_date'],
                    task['end_date'],
                    task['total_work_hours'],
                    task['status'],
                    task['project']
                    ]
                dataframe.append(detail)
            summary_row: list = ['', '', '', person_total_work_hours, '', '']
            dataframe.append(summary_row)
            df = pd.DataFrame(dataframe, columns=headers)
            default_style = self.set_default_style()
            sf = StyleFrame(df, styler_obj=default_style)
            self.set_header_style(sf)
            self.set_column_style(sf)
            self.set_column_width(sf)
            sf.to_excel(excel_writer, sheet_name=person_name)
        excel_writer.save()
    
    
    def set_default_style(self):
        default_style = Styler(
            horizontal_alignment='center',
            vertical_alignment='top',
            font=utils.fonts.calibri,  # Add font format
            font_size=13
            )
        return default_style
    
    
    def set_header_style(self, sf):
        header_style = Styler(
            horizontal_alignment='center',
            vertical_alignment='center',
            bg_color=utils.colors.dark_green,
            bold=True,
            font=utils.fonts.calibri,  # Add font format
            font_size=15
            )
        sf.apply_headers_style(styler_obj=header_style)
    
    
    def set_column_style(self, sf):
        # add column style follow header
        header_list: list = ['Title']
        column_style = Styler(
            horizontal_alignment='left',
            vertical_alignment='top'
            )
        sf.apply_column_style(cols_to_style=header_list, styler_obj=column_style)
        
    
    def set_column_width(self, sf):
        column_header_set: list = list(REPORT_HEADER.keys())
        for header in column_header_set:
            sf = sf.set_column_width(columns=[header], width=REPORT_HEADER[header])
            

## For Test
# generator = GenerateExcel()
# dict_data = generator.get_dict_data_from_jsonfile('./export_data.json')
# generator.write_excel(dict_data)
