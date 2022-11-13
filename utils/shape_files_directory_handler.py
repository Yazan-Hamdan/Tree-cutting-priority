import os

from osgeo import ogr


class ShapeFilesDirectoryHandler:
    def __init__(self, directory_name: str):
        """
        Args:
            directory_name:[str] The name of directory where shapefiles are
                                 stored
        """
        # get path of the base directory
        base_dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # join base_dir_path with the data_directory
        self.__directory_path = os.path.join(base_dir_path,
                                             f'{directory_name}')

    def __get_shapefiles(self) -> list:
        """
        return all shapefiles of a directory
        Returns:
            shape_files: [list] all shapefiles into one list
        """
        shape_files = [f for f in os.listdir(self.__directory_path) if
                       f.endswith('.shp')]
        return shape_files

    def read_shapefiles(self) -> dict:
        """
        open a list of shapefiles into one list

        Returns: files_data: [dict] where key is the name of the file,
                                    value is the data stored in that file

        Note:

        """
        shape_files = self.__get_shapefiles()
        files_data = {
            filename: ogr.Open(os.path.join(self.__directory_path, filename))
            for filename in shape_files}
        return files_data
