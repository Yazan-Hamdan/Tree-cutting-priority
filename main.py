from utils.shape_files_directory_handler import ShapeFilesDirectoryHandler
from osgeo import gdal
import argparse


def rasterize_shapefile(shape_file, raster_file_name, call_back, **args):
    '''
        Rasterize vector shape file.
        Args:
            shape_file: The shape file to rasterize.
            raster_file_name: The output filename of the raster.
            call_back: optional call back function after rasterization.
            args: Extra arguments to the rasterization method.
    '''
    pixel_size = 25
    no_data_value = -9999
    x_res = 230
    y_res = 221
    x_min = 522556.47860572586
    # x_max = 528313.1113211802
    # y_min = 3780732.388856534
    y_max = 3786279.2744338084

    # Open the data source and read in the extent
    source_layer = shape_file.GetLayer()

    target_ds = gdal.GetDriverByName('GTiff').Create(
        raster_file_name, x_res, y_res, 1, gdal.GDT_Int16)
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(no_data_value)

    # Rasterize
    gdal.RasterizeLayer(target_ds, [1], source_layer, **args)

    call_back(target_ds)


def calculate_raster_distance(target_ds):
    '''
        Calculate Euclidean Distance for the raster.
        Args:
            target_ds: The created GeoTiff file.
    '''
    band = target_ds.GetRasterBand(1)
    gdal.ComputeProximity(band, band, options=['VALUES=0'])


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-sp",
        "--shape_path",
        help="The absolute path to the shape files.",
        required='true')

    cmd_args = arg_parser.parse_args()

    file_handler = ShapeFilesDirectoryHandler(cmd_args.shape_path)
    shape_files = file_handler.read_shapefiles()

    egress_shape_file = shape_files["EgressRoutes"]

    rasterize_shapefile(egress_shape_file, "testy2.tiff",
                        calculate_raster_distance, burn_values=[0])
    # rasterize_shapefile(egress_shape_file, "testy.tiff", options=[
    #     'ATTRIBUTE=pop_per_sq'])

    print(shape_files)
