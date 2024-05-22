import os

class Utils:
    @staticmethod
    def get_absolute_file_path(file_name):
        project_path = os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(project_path):
            if file_name in files:
                return os.path.join(root, file_name)


if __name__ == "__main__":
    pass
