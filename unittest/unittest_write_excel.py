import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from write_excel import GenerateExcel


class testReadExcelData(unittest.TestCase):
    def setUp(self) -> None:
        self.generater = GenerateExcel()
        self.file_path: str = r'./data/get_data-testExportData.json'
        self.file_invalid_path: str = r'./data/test.json'
        self.file_invalid_extension: str = r'./data/test.txt'

    def test_readFile_success(self):
        data_from_json_file: dict = self.generater.get_dict_data_from_jsonfile(self.file_path)
        self.assertIsInstance(data_from_json_file, dict)
        self.assertTrue(os.path.exists(self.file_path))

    def test_readFile_noFound(self):
        self.assertRaises(FileNotFoundError,
                        self.generater.get_dict_data_from_jsonfile,
                        self.file_invalid_path)

    def test_readFile_invalidExtFile(self):
        self.assertRaises(ValueError,
                          self.generater.get_dict_data_from_jsonfile,
                          self.file_invalid_extension)


if __name__=='__main__':
    unittest.main()
