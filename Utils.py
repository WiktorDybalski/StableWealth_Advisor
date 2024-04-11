import os


class Utils:
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    project_structure_dict = {"stock_data.csv": "Data", "CalculatorStyle.qss": "GUI/Styles",
                              "HomeWindowStyle.qss": "GUI/Styles", "SharesAssistantStyle.qss": "GUI/Styles"}

    @staticmethod
    def get_absolute_file_path(file_name):
        absolute_file_path = os.path.join(Utils.PROJECT_PATH, Utils.project_structure_dict.get(file_name), file_name)
        absolute_file_path = absolute_file_path.replace('\\', '/')
        return absolute_file_path


print(Utils.get_absolute_file_path("SharesAssistantStyle.qss"))