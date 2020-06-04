import ee

ee.Initialize()


def select_data(source, lon, lat, start, end, bands):

    """
    WIP: Currently only works for a point location.

    creates an image collection and filters it as per the requested data.

    Arguments:

    source (str) -- ID of the dataset to be downloaded from GEE

    start (str) -- starting date of the dataset request in the form YYYY-MM-DD

    end (str) -- ending date of the dataset request in the form YYYY-MM-DD

    bands (list of str) -- bands requested from the datset 


    """

    data = ee.ImageCollection(source)
    filtered_data = (
        data.filterDate(start, opt_end=end)
        .select(bands)
        .filterBounds(ee.Geometry.Point(lon, lat))
    )
    final_data = filtered_data.getInfo()
