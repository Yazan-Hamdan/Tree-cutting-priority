import os

from osgeo import ogr


class ShapeFilesDirectoryHandler:
    def __init__(self, directory_name: str):
        """
        Args:
            directory_name:[str] The name of directory where shapefiles are stored
        """
        # get path of the base directory
        base_dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # join base_dir_path with the data_directory
        self.__directory_path = os.path.join(base_dir_path, f'{directory_name}')

    def __get_shapefiles(self) -> list:
        shape_files = [f for f in os.listdir(self.__directory_path) if f.endswith('.shp')]
        return shape_files

    def read_shapefiles(self) -> dict:
        shape_files = self.__get_shapefiles()
        files_data = {filename: ogr.Open(filename) for filename in shape_files}
        return files_data
