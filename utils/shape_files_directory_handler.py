import os

from osgeo import ogr


class ShapeFilesDirectoryHandler:
    def __init__(self, directory_path: str):
        # get path of the base directory
        base_dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # join base_dir_path with the data_directory
        self.__directory_path = os.path.join(base_dir_path, f'{directory_path}')

    def __get_shapefiles(self) -> list:
        shape_files = [f for f in os.listdir(self.__directory_path) if f.endswith('.shp')]
        return shape_files

    def read_shapefiles(self):
        shape_files = self.__get_shapefiles()
        files_data = {filename: ogr.Open(filename) for filename in shape_files}
        return files_data
