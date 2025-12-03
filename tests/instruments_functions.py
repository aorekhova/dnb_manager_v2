import unittest
import instruments.prepare_parameters as absolut_path



class MyTestCase(unittest.TestCase):
    def test_convert_absolute_path(self):
        template = "%TEN_SOURCES%\%TASK_NAME%"
        task_name = "2025-OCT"

        result = absolut_path.convert_absolute_path(template, task_name)
        print(result)

        assert result == r"C:/reports/TeN/sources\2025-OCT"


    def test_convert_absolute_path_v2(self):
        template = "%APS_SELECTED_PARTIES%/%TASK_NAME%/APS-buyers-%MONTH%.csv"
        task_name = "2025-OCT"
        month = "october"

        result = absolut_path.convert_absolute_path(template, task_name, month)
        print(result)

        assert result == r"C:/reports/APS/selected_parties/2025-OCT/APS-buyers-october.csv"


    def test_convert_absolute_path_v3(self):
        template = "APS"
        task_name = "2025-OCT"
        month = "october"

        result = absolut_path.convert_absolute_path(template, task_name, month)
        print(result)

        assert result == r"APS"




if __name__ == '__main__':
    unittest.main()
