import os

# TODO
# fix Utils class
class Utils:
    @staticmethod
    def get_absolute_file_path(file_name):
        project_path = os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(project_path):
            if file_name in files:
                return os.path.join(root, file_name)
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
