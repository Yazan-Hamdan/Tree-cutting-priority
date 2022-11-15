from osgeo import gdal
import argparse
import numpy as np

from utils.shape_files_directory_handler import ShapeFilesDirectoryHandler

NO_DATA_VALUE = -9999


def get_classification_ranges(min_val, max_val) -> list[tuple[float, float]]:
    """ Splits values into ranges to classify into 9 categories.

    Args:
        min (number): Minimum values of the data.
        max (number): Maximum value of the data.

    Returns:
        list[tuple[float, float]]: The ranges to classify with.
    """
    data_range = (max_val - min_val) / 9
    return [(min_val + (data_range * i), min_val + (data_range * (i + 1)))
            for i in range(0, 9)]


def classify_band(band) -> None:
    """ Classify raster band values.

    Args:
        band: The band to classify.
    """
    [data_min, data_max, _, __] = band.GetStatistics(True, True)

    band_data = np.array(band.ReadAsArray())
    final_data = band_data.copy()
    ranges = get_classification_ranges(data_min, data_max)
    current_class = 1

    for val_range in ranges:
        data_selection = \
            (final_data >= val_range[0]) & (final_data < val_range[1]) \
            if val_range[0] != ranges[-1][0] else \
            (final_data >= val_range[0]) & (final_data <= val_range[1])

        final_data[data_selection] = current_class
        current_class += 1

    band.WriteArray(final_data)


def rasterize_shapefile(
    shape_file,
    raster_file_name,
    call_back,
    **args
) -> gdal.Dataset:
    """ Rasterize vector shape file.

        Args:
            shape_file: The shape file to rasterize.
            raster_file_name: The output filename of the raster.
            call_back: Optional call back function after rasterization.
            args: Extra arguments to the rasterization method.

        Returns:
            gdal.Dataset: The raster as a GDAL Dataset.
    """
    pixel_size = 25
    x_res = 230
    y_res = 221
    x_min = 522556.47860572586
    y_max = 3786279.2744338084

    source_layer = shape_file.GetLayer()

    target_ds: gdal.Dataset = gdal.GetDriverByName('GTiff').Create(
        raster_file_name, x_res, y_res, 1, gdal.GDT_Float32)
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NO_DATA_VALUE)

    # Rasterize
    gdal.RasterizeLayer(target_ds, [1], source_layer, **args)

    if call_back:
        call_back(target_ds)

    return target_ds


def calculate_raster_distance(target_ds):
    """ Calculate Euclidean Distance for the raster.

        Args:
            target_ds: The created GeoTiff file.
    """
    band = target_ds.GetRasterBand(1)
    gdal.ComputeProximity(band, band, options=[
                          'VALUES=0', 'DISTUNITS=GEO', 'MAXDIST=100'])
    classify_band(band)


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

    egress_shape_file = shape_files["PopulatedAreast"]

    # Radius data
    # rasterize_shapefile(egress_shape_file, "test.tif",
    #                     calculate_raster_distance, burn_values=[0])

    # Data with values included
    rasterize_shapefile(
        egress_shape_file,
        "testy.tiff",
        lambda target_ds: classify_band(target_ds.GetRasterBand(1)),
        options=['ATTRIBUTE=pop_per_sq']
    )

    print(shape_files.keys())
