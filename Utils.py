import os

# TODO
# fix Utils class
class Utils:
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    project_structure_dict = {"stock_data.csv": "Data", "stock_data_reduced.csv": "Data",
                              "stock_data_without_polish.csv": "Data", "stock_data_without_polish_reduced.csv": "Data",
                              "CalculatorStyle.qss": "GUI/Styles",
                              "HomeWindowStyle.qss": "GUI/Styles", "SharesAssistantStyle.qss": "GUI/Styles",
                              "SharesAssistantResultsStyle.qss": "GUI/Styles", "recently_updated_day.txt": "Data",
                              "new_stock_data.csv": "Data", "new_stock_data_reduced.csv": "Data",
                              "down_red.png": "Images", "up_green.png": "Images", "StockInformationStyle.qss": "GUI/Styles",
                              "chart_icon.png": "Images"}
    @staticmethod
    def add_file_path(file_name):
        pass

    @staticmethod
    def is_in_dict(file_name):
        return file_name in Utils.project_structure_dict
    @staticmethod
    def get_absolute_file_path(file_name):
        absolute_file_path = os.path.join(Utils.PROJECT_PATH, Utils.project_structure_dict.get(file_name), file_name)
        if Utils.is_in_dict(file_name):
            absolute_file_path = absolute_file_path.replace('\\', '/')
        else:
            absolute_file_path = Utils.add_file_path(file_name)
        return absolute_file_path

if (__name__ == "__main__" ):
    pass


#
# class Utils:
#     @staticmethod
#     def get_absolute_file_path(file_name):
#         # Pobierz folder domowy użytkownika
#         home_dir = os.path.expanduser("~")
#
#         # Utwórz ścieżkę do folderu python wewnątrz katalogu domowego
#         python_folder = os.path.join(home_dir, "python")
#
#         # Upewnij się, że folder istnieje
#         os.makedirs(python_folder, exist_ok=True)
#
#         # Połącz nazwę pliku z pełną ścieżką folderu python
#         absolute_path = os.path.join(python_folder, file_name)
#
#         return absolute_path
#
#
# # Przykład użycia:
# file_path = Utils.get_absolute_file_path("example.txt")
# print(f"Absolute file path: {file_path}")
