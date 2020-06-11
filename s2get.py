import satellitetools.gee as gee
import satellitetools.biophys_xarray as bio
import geopandas as gpd
import os


def s2_ndvi(geofile, outdir, choice, start, end, qi_threshold):
    """ 
    Downloads sentinel 2 data and calculates one of NDVI, LAI, FAPAR. All of these are performed using satellitetools created by Olli Nevalainen.
    
    Parameters
    ----------
    
    geofile (str) -- path to the file containing the coordinates of AOI, currently tested with geojson 
    
    outdir (str) -- path to the directory where the output file is stored. If specified directory does not exists, it is created.
    
    choice (str) -- NDVI, LAI, FAPAR
    
    start (str) -- starting date of the data request in the form YYYY-MM-DD
    
    end (str) -- ending date of the data request in the form YYYY-MM-DD
    
    qi_threshold (float) -- From satellitetools: Threshold value to filter images based on used qi filter. qi filter holds labels of classes whose percentages within the AOI is summed. If the sum is 				     larger then the qi_threhold, data will not be retrieved for that date/image. The default is 1, meaning all data is retrieved
        
 
    Returns
    -------
    Nothing:
            output netCDF is stored in the specified directory.
    
    """

    # convert user's choice to lowercase so that function arguments are case-insensitive
    choice = choice.lower()

    # if requested choice is not available raise an value error.
    if choice not in ["ndvi", "lai", "fapar"]:
        raise ValueError("choice must be one of NDVI, LAI, FAPAR")

    # read in the input file containing coordinates
    df = gpd.read_file(geofile)

    request = gee.S2RequestParams(start, end)

    # filter area of interest from the coordinates in the input file
    area = gee.AOI(df[df.columns[0]].iloc[0], df[df.columns[1]].iloc[0])

    # calcuate qi attribute for the AOI
    gee.ee_get_s2_quality_info(area, request)

    # get the final data
    gee.ee_get_s2_data(area, request, qi_threshold=qi_threshold)

    # convert dataframe to an xarray dataset, used later for converting to netCDF
    gee.s2_data_to_xarray(area, request)

    # perform the computation for the selected choice using SNAP
    if choice == "ndvi":
        area.data = bio.compute_ndvi(area.data)
    elif choice == "lai":
        area.data = bio.run_snap_biophys(area.data, "LAI")
    else:
        area.data = bio.run_snap_biophys(area.data, "FAPAR")

    timeseries = {}
    timeseries_variables = [choice]

    # is specified output directory does not exist, create it.
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    # creating a timerseries and saving the netCDF file
    area.data.to_netcdf(os.path.join(outdir, area.name + ".nc"))
    timeseries[area.name] = gee.xr_dataset_to_timeseries(
        area.data, timeseries_variables
    )


s2_ndvi(
    "./satellitetools/geometry-files/test.geojson",
    "./out/",
    "ndvi",
    start="2019-01-01",
    end="2019-12-31",
    qi_threshold=1,
)
