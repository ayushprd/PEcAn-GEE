import concurrent.futures
import time
from remote_process import remote_process

tstart = time.perf_counter()


geofile_list = [
    "./satellitetools/test.geojson",
    "./satellitetools/test2.geojson",
    "./satellitetools/test3.geojson",
]

outdir_list = ["./out", "./out", "./out"]

start_list = ["2018-01-01", "2019-01-01", "2018-01-01"]

end_list = ["2018-12-31", "2019-12-31", "2018-12-31"]

source_list = ["gee", "gee", "gee"]

collection_list = ["COPERNICUS/S2_SR", "NASA_USDA/HSL/SMAP_soil_moisture", "LANDSAT/LC08/C01/T1_SR"]

scale_list = [10, None, 30]

qc_list = [1, None, 1]

algorithm_list = ["snap", "snap", "snap"]

output_list = [
    {"get_data": "bands", "process_data": "lai"},
    {"get_data": "bands", "process_data": "lai"},
    {"get_data": "bands", "process_data": "lai"},
]

stage_list = [
    {"get_data": True, "process_data": True},
    {"get_data": True, "process_data": False},
    {"get_data": True, "process_data": False},
]

#with concurrent.futures.ProcessPoolExecutor() as executor:
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(
        remote_process,
        geofile_list,
        outdir_list,
        start_list,
        end_list,
        source_list,
        collection_list,
        scale_list,
        qc_list,
        algorithm_list,
        output_list,
        stage_list,
    )

tfinish = time.perf_counter()

print("finished in {}".format(tfinish - tstart))
