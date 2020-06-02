import ee
from datetime import datetime


ee.Initialize()


def sanity_check(source, start, end, bands):

    """
    Checks if requested data is available on Google Earth Engine

    Arguments:

    source (str) -- ID of the dataset to be downloaded from GEE

    start (str) -- starting date of the dataset request in the form YYYY-MM-DD

    end (str) -- ending date of the dataset request in the form YYYY-MM-DD

    bands (list of str) -- bands requested from the datset 

    Returns:

    bool - TRUE if data is available for the requested daterange and bands

    """

    # creating a image collection using the requested dataset ID
    img_collection = ee.ImageCollection(source)

    # creating a image by selecting the first image from image collection
    single_img = ee.Image(img_collection.first())

    # sorting the images
    first_img = ee.Image(img_collection.sort("system:time_start").first())
    last_img = ee.Image(img_collection.sort("system:time_start", False).first())

    # selecting date (str) from the metadata the first image
    first_img_date = (
        ee.Date(first_img.get("system:time_start")).format("Y-M-d").getInfo()
    )

    # selecting date (str) from the metadata the last image
    last_img_date = ee.Date(last_img.get("system:time_start")).format("Y-M-d").getInfo()

    # creating datetime objects from dates extracted from the dataset
    first_img_date = datetime.strptime(first_img_date, "%Y-%m-%d")
    last_img_date = datetime.strptime(last_img_date, "%Y-%m-%d")

    # creating datetime objects from dates provided by the user
    user_start_date = datetime.strptime(start, "%Y-%m-%d")
    user_end_date = datetime.strptime(end, "%Y-%m-%d")

    # all the bands available in the requested dataset
    bands_available = single_img.bandNames().getInfo()

    # checking if the requested bands are available in the dataset and data for requested daterange is present
    if all(i in bands_available for i in bands) and (
        first_img_date <= user_start_date and user_end_date <= last_img_date
    ):
        return True
