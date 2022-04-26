# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Accelerating Lagrangian analyses of oceanic data: benchmarking typical workflows

# + [markdown] tags=[]
# ## Authors
# -

Author1 = {"name": "Miron, Philippe", "affiliation": "Florida State University", "email": "pmiron@fsu.edu", "orcid": "0000-0002-8520-6221"}
Author2 = {"name": "Elipot, Shane", "affiliation": "University of Miami", "email": "selipot@miami.edu", "orcid": "0000-0001-6051-5426 "}
Author3 = {"name": "Lumpkin, Rick", "affiliation": "NOAA’s Atlantic Oceanographic and Meteorological Laboratory", "email": "rick.lumpkin@noaa.gov", "orcid": "0000-0002-6690-1704 "}
Author4 = {"name": "Dano, Bertrand", "affiliation": "NOAA’s Atlantic Oceanographic and Meteorological Laboratory", "email": "danob@miami.edu", "orcid": "0000-0002-3372-2566"}

# + [markdown] tags=[] toc=true
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc">
#     <ul class="toc-item">
#         <li>
#             <span>
#                 <a href="#Accelerating-Lagrangian-analyses-of-oceanic-data:-benchmarking-typical-workflows" data-toc-modified-id="Accelerating Lagrangian analyses of oceanic data: benchmarking typical workflows">
#                     <span class="toc-item-num">1.&nbsp;</span>Accelerating Lagrangian analyses of oceanic data: benchmarking typical workflows
#                 </a>
#             </span>
#             <ul class="toc-item">
#                 <li>
#                     <span>
#                         <a href="#Authors" data-toc-modified-id="Authors"><span class="toc-item-num">1.1&nbsp;</span>Authors</a>
#                     </span>
#                 </li>
#             </ul>
#         </li>
#         <li>
#             <span>
#                 <a href="#Table-of-Content" data-toc-modified-id="Table of Content"> <span class="toc-item-num">2.&nbsp;</span>Table of Content </a>
#             </span>
#         </li>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Purpose" data-toc-modified-id="Purpose"><span class="toc-item-num">2.1&nbsp;</span>Purpose</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Technical-contributions" data-toc-modified-id="Technical-contributions"><span class="toc-item-num">2.2&nbsp;</span>Technical contributions</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Methodology" data-toc-modified-id="Methodology"><span class="toc-item-num">2.4&nbsp;</span>Methodology</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Results" data-toc-modified-id="Results"><span class="toc-item-num">2.4&nbsp;</span>Results</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Funding" data-toc-modified-id="Funding"><span class="toc-item-num">2.5&nbsp;</span>Funding</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Keywords" data-toc-modified-id="Keywords"><span class="toc-item-num">2.6&nbsp;</span>Keywords</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Citation" data-toc-modified-id="Citation"><span class="toc-item-num">2.7&nbsp;</span>Citation</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Acknowledgements" data-toc-modified-id="Acknowledgements"><span class="toc-item-num">2.8&nbsp;</span>Acknowledgements</a>
#                 </span>
#             </li>
#         </ul>
#         <li>
#             <span>
#                 <a href="#Setup" data-toc-modified-id="Setup"><span class="toc-item-num">3.&nbsp;</span>Setup</a>
#             </span>
#         </li>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Library-import" data-toc-modified-id="Library-import"><span class="toc-item-num">3.1&nbsp;</span>Library import</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Local-library-import" data-toc-modified-id="Local-library-import"><span class="toc-item-num">3.2&nbsp;</span>Local library import</a>
#                 </span>
#             </li>
#         </ul>
#         <li>
#             <span>
#                 <a href="#Data-Overview" data-toc-modified-id="Data Overview"><span class="toc-item-num">4.&nbsp;</span>Data Overview</a>
#             </span>
#         </li>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Individual-NetCDFs" data-toc-modified-id="Individual NetCDFs"><span class="toc-item-num">4.1&nbsp;</span>Individual NetCDFs</a>
#                 </span>
#             </li>
#             <ul class="toc-item">
#               <li>
#                   <span>
#                       <a href="#Dimensions" data-toc-modified-id="Dimensions"><span class="toc-item-num">4.1.1&nbsp;</span>Dimensions</a>
#                   </span>
#               </li>
#               <li>
#                   <span>
#                       <a href="#Variables" data-toc-modified-id="Variables"><span class="toc-item-num">4.1.2&nbsp;</span>Variables</a>
#                   </span>
#               </li>
#             </ul>
#             <li>
#                 <span>
#                     <a href="#Contiguous-Ragged-Array" data-toc-modified-id="Contiguous Ragged Array"><span class="toc-item-num">4.2&nbsp;</span>Contiguous Ragged Array</a>
#                 </span>
#             </li>
#         </ul>
#         <li>
#         <span>
#             <a href="#Xarray" data-toc-modified-id="Xarray"><span class="toc-item-num">5.&nbsp;</span>Xarray</a>
#         </span>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Xarray-test-1:-Geographical-binning-of-any-variable" data-toc-modified-id="Xarray test 1: Geographical binning of any variable"><span class="toc-item-num">5.1&nbsp;</span>Xarray test 1: Geographical binning of any variable</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Xarray-test-2:-Extract-a-given-region" data-toc-modified-id="Xarray test 2: Extract a given region"><span class="toc-item-num">5.2&nbsp;</span>Xarray test 2: Extract a given region</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Xarray-test-3:-Operations-per-trajectory" data-toc-modified-id="Xarray test 3: Operations per trajectory"><span class="toc-item-num">5.3&nbsp;</span>Xarray test 3: Operations per trajectory</a>
#                 </span>
#             </li>
#         <ul class="toc-item">
#             <li>
#         <span>
#             <a href="#Single-statistic-per-trajectory" data-toc-modified-id="Single statistic per trajectory"><span class="toc-item-num">5.3.1&nbsp;</span>Single statistic per trajectory</a>
#         </span>
#             </li>
#             <li>
#         <span>
#             <a href="#Operations-per-trajectory" data-toc-modified-id="Operations per trajectory"><span class="toc-item-num">5.3.2&nbsp;</span>Operations per trajectory</a>
#         </span>
#             </li>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Simple-operation-by-chunks-(or-blocks)" data-toc-modified-id="Simple operation by chunks (or blocks)"><span class="toc-item-num">5.3.1.1&nbsp;</span>Simple operation by chunks (or blocks)</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#More-complex-operation-where-dimensions-can-change-between-input-and-output" data-toc-modified-id="More complex operation where dimensions can change between input and output"><span class="toc-item-num">5.3.1.2&nbsp;</span>More complex operation where dimensions can change between input and output</a>
#                 </span>
#             </li>
#         </ul>
#         </ul>
#         </ul>
#         <li>
#         <span>
#             <a href="#Pandas" data-toc-modified-id="Pandas"><span class="toc-item-num">6.&nbsp;</span>Pandas</a>
#         </span>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Pandas-test-1:-Geographical-binning-of-any-variable" data-toc-modified-id="Pandas test 1: Geographical binning of any variable"><span class="toc-item-num">6.1&nbsp;</span>Pandas test 1: Geographical binning of any variable</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Pandas-test-2:-Extract-a-given-region" data-toc-modified-id="Pandas test 2: Extract a given region"><span class="toc-item-num">6.2&nbsp;</span>Pandas test 2: Extract a given region</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Pandas-test-3:-Single-statistic-per-trajectory" data-toc-modified-id="Pandas test 3: Single statistic per trajectory"><span class="toc-item-num">6.3&nbsp;</span>Pandas test 3: Single statistic per trajectory</a>
#                 </span>
#             </li>
#         </ul>
#         </li>
#         <li>
#         <span>
#             <a href="#Awkward-Array" data-toc-modified-id="Awkward Array"><span class="toc-item-num">7.&nbsp;</span>Awkward Array</a>
#         </span>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Awkward-Array-test-1:-Geographical-binning-of-any-variable" data-toc-modified-id="Awkward Array test 1: Geographical binning of any variable"><span class="toc-item-num">7.1&nbsp;</span>Awkward Array test 1: Geographical binning of any variable</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Awkward-Array-test-2:-Extract-a-given-region" data-toc-modified-id="Awkward Array test 2: Extract a given region"><span class="toc-item-num">7.2&nbsp;</span>Awkward Array test 2: Extract a given region</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Awkward-Array-test-3:-Single-statistic-per-trajectory" data-toc-modified-id="Awkward Array test 3: Single statistic per trajectory"><span class="toc-item-num">7.3&nbsp;</span>Awkward Array test 3: Single statistic per trajectory</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Numba" data-toc-modified-id="Numba"><span class="toc-item-num">7.4&nbsp;</span>Numba</a>
#                 </span>
#             </li>
#         </ul>
#         </li>
#         <li>
#         <span>
#             <a href="#Discussion" data-toc-modified-id="Discussion"><span class="toc-item-num">8.&nbsp;</span>Discussion</a>
#         </span>
#         <ul class="toc-item">
#             <li>
#                 <span>
#                     <a href="#Benchmark-speed" data-toc-modified-id="Benchmark speed"><span class="toc-item-num">8.1&nbsp;</span>Benchmark speed</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Feedback" data-toc-modified-id="Feedback"><span class="toc-item-num">8.2&nbsp;</span>Feedback</a>
#                 </span>
#             </li>
#             <li>
#                 <span>
#                     <a href="#Future-development" data-toc-modified-id="Future development"><span class="toc-item-num">8.3&nbsp;</span>Future development</a>
#                 </span>
#             </li>
#         </ul>
#         </li>
#         <li>
#         <span>
#             <a href="#References" data-toc-modified-id="References"><span class="toc-item-num">9.&nbsp;</span>References</a>
#         </span>
#         </li>
#     </ul>
# </div>
# -

# ## Purpose
#
# For data, *Lagrangian* refers to oceanic and atmosphere information acquired by observing platforms drifting with the flow they are embedded within, but also refers more broadly to the data originating from uncrewed platforms, vehicles, and animals that gather data along their unrestricted and often complex paths. Because such paths traverse both spatial and temporal dimensions, Lagrangian data often convolve spatial and temporal information that cannot always readily be organized in common data structures and stored in standard file formats with the help of common libraries and standards. As such, for both originators and users, Lagrangian data present challenges that the [EarthCube CloudDrift](https://github.com/Cloud-Drift) project aims to overcome.
#
# This notebook consists of systematic evaluations and comparisons of workflows for Lagrangian data, using as a basis the velocity and sea surface temperature datasets emanating from the drifting buoys of the [Global Drifter Program](https://www.aoml.noaa.gov/phod/gdp/) (GDP). Specifically, we consider the interplay between diverse storage file formats ([NetCDF](https://www.unidata.ucar.edu/software/netcdf/), [Parquet](https://github.com/apache/parquet-format)) and the data structure associated with common existing libraries in *Python* ([xarray](https://docs.xarray.dev/en/stable/), [pandas](https://pandas.pydata.org), and [Awkward Array](https://awkward-array.org/quickstart.html)) in order to test their adequacies for performing three common Lagrangian tasks:
#
# 1. binning of a variable on an spatially-fixed grid (e.g. mean temperature map),
# 2. extracting data within given geographical and/or temporal windows (e.g. Gulf of Mexico),
# 3. analyses per trajectory (e.g. single statistics, spectral estimation by Fast Fourier Transform).
#
# Since the *CloudDrift* project aims at accelerating the use of Lagrangian data for atmospheric, oceanic, and climate sciences, we hope that the users of this notebook will provide us with feedback on its ease of use and the intuitiveness of the proposed methods in order to guide the on-going development of the *clouddrift* *Python* package.
#
# ## Technical contributions
#
# - Description of some challenges arising from the analysis of large, heterogeneous Lagrangian datasets.
# - Description of some data formats for Lagrangian analysis with *Python*.
# - Comparison of performances of established and developing *Python* packages and libraries.
#
# ## Methodology
#
# The notebook proceeds in three steps:
# 1. First, we download a subset of the hourly dataset of the GDP. Specifically, we access version 2.00 (beta) of the dataset that consists of a collection of 17,324 NetCDF files, one for each drifting buoy, available from a HHTPS (or FTP) [server](https://www.aoml.noaa.gov/ftp/pub/phod/lumpkin/hourly/v2.00/netcdf/) of the GDP. Alternative methods to download these data are described on the website of the [GDP DAC at NOAA AOML](https://www.aoml.noaa.gov/phod/gdp/hourly_data.php) and includes a newly-formed collection from the NOAA National Centers for Environmental Information with [doi:10.25921/x46c-3620](https://doi.org/10.25921/x46c-3620). We download a subset (which size can be scaled up or down) then proceed to aggregate the data from the individual files in one single file using a suggested format (the contiguous ragged array).
#
# 2. Second, we benchmark three libraries—*xarray*, *Pandas*, and *Awkward Array*—with typical Lagrangian workflow tasks such as the geographical binning of a variable, the extraction of the data for a given region, and operations performed per drifter trajectory.
#
# 3. Third, we discuss briefly future works for the upcoming *clouddrift* library, and seek to obtain feedback from the community to guide future development.
#
# ## Results
#
# In terms of data file format, we tested both NetCDF and Parquet file formats but did not find significant performance gain from using one or the other. Because NetCDF is a well-known and established file format in Earth sciences, we save the contiguous ragged array as a single NetCDF archive. 
#
# In terms of python packages, we find that *Pandas* is intuitive with a simple syntax but does not perform efficiently with a large dataset. The complete GDP hourly dataset is currently *only* ~15 GB, but as part of *CloudDrift* we also want to support larger Lagrangian datasets (>100 GB). On the other hand, *xarray* can interface with *Dask* to efficiently *lazy-load* large dataset but it requires custom adaptation to operate on a ragged array. In contrast, *Awkward Array* provides a novel approach by storing alongside the data an offset index in a manner that is transparent to the user, simplifying the analysis of non-uniform Lagrangian datasets. We find that it is also *fast* and can easily interface with *Numba* to further improve performances.
#
# In terms of benchmark speed, each package show similar results for the geographical binning (test 1) and the operation per trajectory (test 3) benchmarks. For the extraction of a given region (test 2), *xarray* was found to be slower than both *Pandas* and *Awkward Array*. We note that speed performance may not the deciding factor for all users and we believe that ease of use and simple intuitive syntax are also important.

# ## Funding

Award1 = {"agency": "NSF EarthCube", "award_code": "2126413", "award_URL": "https://www.nsf.gov/awardsearch/showAward?AWD_ID=2126413"}
Award2 = {"agency": "Atlantic Oceanographic and Meteorological Laboratory", "award_code": "", "award_URL": "https://www.aoml.noaa.gov/global-drifter-program"}
Award3 = {"agency": "NOAA’s Global Ocean Monitoring and Observing Program", "award_code": "", "award_URL": "https://globalocean.noaa.gov"}

# ## Keywords

keywords=["lagrangian", "drifters", "data structures", "workflow tasks", "benchmarks"]

# + [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ## Citation
#
# P. Miron, S. Elipot, R. Lumpkin and B. Dano, Accelerating Lagrangian analysis of oceanic data: benchmarking typical workflows, 2022, 2022 EarthCube Annual Meeting, Accessed X/Y/2022 at https://github.com/Cloud-Drift/earthcube-meeting-2022
#
# ## Acknowledgements
#
# The CloudDrift team would like to acknowledge [Dr. Ryan Abernathey](https://github.com/rabernat) for suggesting to create benchmarks on typical Lagrangian workflow tasks and [Dr. Jim Pivarski](https://github.com/jpivarski) for assisting with Awkward array.
# -

# # Setup
#
# ## Library import

# +
# Data manipulation
import numpy as np
import xarray as xr
import pandas as pd
import awkward as ak
from scipy import stats

# others
import time
from os.path import isfile, join
from datetime import datetime
import dask
import numba as nb
import functools

# data retrieval
import urllib.request
import concurrent.futures 
import re

# visualization
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
import cmocean

# we will see that the GDP DAC netcdf files contain non standard values that cause warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# default settings visualization
plt.rcParams.update({'font.size': 8, 
                     'xtick.major.pad': 1, 
                     'ytick.major.pad': 1})

# system information
import platform
import psutil
# -

# ## Local library import

# To run this notebook, we need to load on a number of functions from the `preprocess.py` file found within this repository.
from preprocess import create_ragged_array, create_ak

# # Data Overview
#
# In the first step of this notebook, we present the current format of the [Global Drifter Program (GDP)](https://www.aoml.noaa.gov/phod/gdp/) dataset, and show how to transform it into a single archival file in which each variable is stored in an ragged fashion.
#
# The GDP produces two interpolated datasets of drifter position, velocity and sea surface temperature from more than 20,000 drifters that have been released since 1979. One dataset is at 6-hour resolution ([Hansen and Poulain 1996](http://dx.doi.org/10.1175/1520-0426(1996)013<0900:QCAIOW>2.0.CO;2)) and the other one is at hourly resolution ([Elipot et al. 2016](http://dx.doi.org/10.1002/2016JC011716)). The files, one per drifter identified by its unique identification number (ID), are updated on a quarterly basis and are available via the [HTTPS server](https://www.aoml.noaa.gov/ftp/pub/phod/lumpkin/hourly/v2.00/netcdf/) of the GDP Data Assembly Center (DAC).
#
# Here we use a subset of the hourly drifter dataset of the GDP by setting the variable `subset_nb_drifters = 500`. The suggested number is large enough to create an interesting dataset, yet without making the downloading cumbersome and the data processing too expensive. Feel free to scale down or up this value (from 1 to 17324), but beware that if you are running this notebook in a binder there is some memory limitation (500 should work). 

subset_nb_drifters = 500  # you can scale up/down this number (maximum value of 17324)

# + tags=[]
# %%time

# output folder and official GDP https server
# Note: If you are running this notebook on a local computer and have already downloaded the individual NetCDF files 
# independently of this notebook, you can move/copy these files to the folder destination shown below, 
# or alternatively change the variable 'folder' to your folder with the data
folder =  'data/raw/'
input_url = 'https://www.aoml.noaa.gov/ftp/pub/phod/lumpkin/hourly/v2.00/netcdf/'

# load the complete list of drifter IDs from the AOML https
urlpath = urllib.request.urlopen(input_url)
string = urlpath.read().decode('utf-8')
pattern = re.compile('drifter_[0-9]*.nc')
filelist = pattern.findall(string)
list_id = np.unique([int(f.split('_')[-1][:-3]) for f in filelist])

# Here we "randomly" select a subset of ID numbers but produce reproducible results
# by actually setting the seed of the random generator
rng = np.random.RandomState(42)  # reproducible results
subset_id = sorted(rng.choice(list_id, subset_nb_drifters, replace=False))

def fetch_netcdf(url, file):
    '''
    Download and save file from the given url (if not present)
    '''
    if not isfile(file):
        req = urllib.request.urlretrieve(url, file)

# Typically it should take ~2 min for 500 drifters
print(f'Fetching the {subset_nb_drifters} requested netCDF files (as a reference ~2min for 500 files).')
with concurrent.futures.ThreadPoolExecutor() as exector:
    # create list of urls and paths
    urls = []
    files = []
    for i in subset_id:
        file = f'drifter_{i}.nc'
        urls.append(join(input_url, file))
        files.append(join(folder, file))
    
    # parallel retrieving of individual netCDF files
    exector.map(fetch_netcdf, urls, files)

# + [markdown] tags=[]
# ## Individual NetCDFs
#
# ### Dimensions
#
# Each individual NetCDF file contains two main dimensions for its variables:
#
# - `['traj']` of length 1, since there is one trajectory per file (e.g. `ID`, `deploy_date`, `deploy_lon`, etc.)
# - `['obs']`: of length N, with N the number of observations along the trajectory (`longitude`, `latitude`, `ve`, `vn`, `sst`, etc.)
#  
# ### Variables
#
# In each file, there are 20 numerical variables representing estimated quantities with dimensions `['traj', 'obs']` (where `traj` = 1 since there is only one trajectory per file). There are 11 numerical variables with dimension `['traj']` that contain metadata unique to each drifter and file (e.g. Deployment date and time). In addition, there are 2 variables with one of their dimensions being `['traj']` that also contains non-numerical metadata (e.g. Buoy type). Further metadata pertaining to an individual drifter and to the whole dataset are contained in various *global attributes* of the NetCDF file.
#
# To have a \"peek\" at the structure of the NetCDF files (dimensions, variables, and attributes), we load the first file in our list of files as an *xarray* dataset object using the `open_dataset`function. *xarray* offers a pleasant html visualization of a dataset (expand the view by clicking on the black arrows to the left).
# -

ds = xr.open_dataset(files[0], decode_times=False)
ds

# + [markdown] tags=[]
# ## Contiguous Ragged Array
#
# In the GDP dataset, the number of observations varies from `len(['obs'])=13` to `len(['obs'])=66417`. As such, it seems inefficient to create bidimensional datastructure `['traj', 'obs']`, commonly used by Lagrangian numerical simulation tools such as [Ocean Parcels](https://oceanparcels.org/) and [OpenDrift](https://opendrift.github.io/) that tend to generate trajectories of equal or similar lengths.
#
# Here, we propose to combine the data from the individual netCDFs files into a [*contiguous ragged array*](https://cfconventions.org/cf-conventions/cf-conventions.html#_contiguous_ragged_array_representation) eventually written in a single NetCDF file in order to simplify data distribution, decrease metadata redundancies, and efficiently store a Lagrangian data collection of uneven lengths. The aggregation process (conducted with the `create_ragged_array` function found in the module `preprocess.py`) also converts to variables some of the metadata originally stored as attributes in the individual NetCDFs. The final structure contains 21 variables with dimension `['obs']` and 38 variables with dimension `['traj']`.
# -

create_ragged_array(files).to_xarray().to_netcdf(join('data', 'gdp_subset.nc'))

# using the previously downloaded files
ds = xr.open_dataset('data/gdp_subset.nc')
ds

# In this `xarray.Dataset` object, the data from the five hundred trajectories (here ordered by ID number by choice) are stored one after the other along the `obs` dimension. To be able to track the sizes of each consecutive trajectory, we have created a new array variable in this dataset called `rowsize` which contains all trajectory lengths.

ds.rowsize

# In summary, we find that the structure of such a contiguous ragged array is perhaps not as straightforward as a two-dimensional array, but nevertheless it has several advantages:
# - Only one file is needed to hold the complete dataset and less storage space is needed than for 2D matrix
# - The extra `rowsize` variable is a small addition to the original data that will be useful to access data per trajectory (see next section)
# - It should be efficient to perform reduce operation (e.g. `mean`, `std`, etc.) on the full dataset since the data is stored in a continuous array.

del ds

# In the second and next step of the notebook, we benchmark different data science *Python* libraries. For this, the following sections present three typical Lagrangian tasks which are conducted successively using *xarray*, *Pandas*, and finally *Awkward Arrays*.

# + [markdown] tags=[]
# # *Xarray*
# -

path_gdp = 'data/gdp_subset.nc'
ds = xr.open_dataset(path_gdp, chunks={}) # chunks={} to automatically select chunks size

# The [xarray](https://docs.xarray.dev/en/stable/) package provides a nice html interface that allows us to quickly scroll to the variables of the xr.Dataset, look at its attributes, and get information about the underlying data structure. Xarray also supports reading the data in *chunks* which are pieces of the underlying data, represented as many *NumPy* (or *NumPy*-like) arrays. The size of the *chunks* is critical to optimize advanced algorithms. Using the default settings (with `chunks={}`), we can see that there is only one chunk per dimension, since the length of one of the variable can easily fit in memory (click on the disk symbol to the right to expand the information and visually see the chunk size).

ds

# + [markdown] tags=[]
# ## *Xarray* test 1: Geographical binning of any variable
# The first benchmark test implemented here is to compute statistics per geographical *bins*. Here we choose to compute the mean of the zonal velocity (`ve`) from all drifter estimates. From the previous cell, we can see that the size of the chunks were automatically set to the size of `obs`, leading to one chunk per variable. For this type of bin operations, one chunk is convenient because the *complete zonal velocity ragged array* variable will be loaded in memory in one operation. In order to perform operations per trajectory (shown below), we will instead set the size of the chunks to be the length of each trajectory, which here would have required `subset_nb_drifters` operation to load the same data.
#
# *Note*: chunks should always aligned with the computation to optimize performance (more details in section 5.3.2).
# -

# In order to keep track of computing times of each test, we create a variable `benchmark_times`.

benchmark_times = np.zeros((3,3))  # 3 benchmark tests for the 3 different processing libraries

# We calculate the mean zonal velocity using the `binned_statistic_2d` function from the `stats` module of the `scipy` package:

# +
t0 = time.time()

lon = np.linspace(-180, 180, 360*2)
lat = np.linspace(-90, 90, 180*2)

ret = stats.binned_statistic_2d(ds.longitude, 
                                ds.latitude,
                                ds.ve,
                                statistic=np.nanmean, 
                                bins=[lon, lat])

benchmark_times[0,0] = time.time() - t0
# -

# We now plot the results:

# +
x_c = np.convolve(lon, [0.5, 0.5], mode='valid')
y_c = np.convolve(lat, [0.5, 0.5], mode='valid')

# get 1st and 99th percentiles of values to plot to get a useful range for the colorscale
v1,v2 = np.nanpercentile(ret.statistic.T,[1,99])

fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.Robinson(central_longitude=-180))
cmap = cmocean.tools.crop(cmocean.cm.balance, vmin=v1, vmax=v2, pivot=0)
pcm = ax.pcolormesh(x_c, y_c, 
                    ret.statistic.T, 
                    cmap=cmap, 
                    transform=ccrs.PlateCarree(),
                    vmin=v1, vmax=v2)

# gridlines and labels
gl = ax.gridlines(color='k', linewidth=0.1, linestyle='-',
                  xlocs=np.arange(-180, 181, 60), ylocs=np.arange(-90, 91, 30),
                  draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# add land and coastline
ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05, axes_class=plt.Axes)
cb = fig.colorbar(pcm, cax=cax);
cb.ax.set_ylabel('Zonal velocity [m/s]');


# -

# ## *Xarray* test 2: Extract a given region
#
# Extracting a subregion of the dataset is also a very common operation. *xarray* provides efficient way to apply mask to the data. One important thing to note is that since we have two dimensions, a mask is applied on the `obs` as well as on the `traj` dimensions. We first define a function to do the data extraction:

def retrieve_region(ds, lon: list = None, lat: list = None, time: list = None) -> xr.Dataset:
    '''Subset the dataset for a region in space and time
    
    Args:
        ds: xarray Dataset
        lon: longitude slice of the subregion
        lat: latitude slice of the subregion
        time: tiem slice of the subregion
    
    Returns: 
        ds_subset: Dataset of the subregion
    '''
    
    # define the mask for the 'obs' dimension
    mask = np.ones(ds.dims['obs'], dtype='bool')

    if lon:
        mask &= (ds.coords['longitude'] >= lon[0]).values
        mask &= (ds.coords['longitude'] <= lon[1]).values

    if lat:
        mask &= (ds.coords['latitude'] >= lat[0]).values
        mask &= (ds.coords['latitude'] <= lat[1]).values

    if time:
        mask &= (ds.coords['time'] >= np.datetime64(time[0])).values
        mask &= (ds.coords['time'] <= np.datetime64(time[1])).values
    
    # define the mask for the 'traj' dimension using the ID numbers from the masked observation
    mask_id = np.in1d(ds.ID, np.unique(ds.ids[mask]))
    ds_subset = ds.isel(obs=np.where(mask)[0], traj=np.where(mask_id)[0])

    return ds_subset.compute()


# Next we use this function to extract the data from the Gulf of Mexico for years 2000 to 2020:

# +
t0 = time.time()

# we need to record the time for benchmarking in the end
lon = [-98, -78]
lat = [18, 31]
day0 = datetime(2000,1,1).strftime('%Y-%m-%d')
day1 = datetime(2020,12,31).strftime('%Y-%m-%d')
days = [day0, day1]
ds_subset = retrieve_region(ds, lon, lat, days)

benchmark_times[0,1] = time.time() - t0
# -

# For visualization of the results, the sea surface temperature estimates along trajectories from the extracted subregion are plotted in the next cell.

# +
fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())

# temperature data are in Kelvin so we convert to degree Celsius
pcm = ax.scatter(ds_subset.longitude, ds_subset.latitude, 
               s=0.05, c=ds_subset.sst-273.15, transform=ccrs.PlateCarree(),
               cmap=cmocean.cm.thermal, vmin=-2, vmax=50)

ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
ax.set_xticks(np.arange(-95, -79, 5), crs=ccrs.PlateCarree())
ax.set_yticks([20, 25, 30], crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='3%', pad=0.02, axes_class=plt.Axes)
cb = fig.colorbar(pcm, cax=cax)
cb.set_label('Sea Surface Temperature [˚C]')
# -

# ## *Xarray* test 3: Operations per trajectory
#
# ### Single statistic per trajectory
# The next type of common operation with Lagrangian data is to compute statistics, or perform time series analysis, per trajectory. In order to do this with an *xarray* dataset, we need to create first a variable that indexes the beginning of each trajectory, i.e. we create an array `traj_idx` in which `traj_idx[i]` is the starting index of the data for the (i+1)<sup>th</sup> trajectory (since *Python* uses zero-based indexing.).

traj_idx = np.insert(np.cumsum(ds.rowsize.values), 0, 0)

# Now, we can retrieve a given variable of a specified trajectory but note that we need to indicate both the start and the end indices of the data for that trajectory. For example, get the SST time series for the 11<sup>th</sup> trajectory:

i = 10
# .compute() is necessary here to explicitely load the data from the file and execute the operation
ds.sst[slice(traj_idx[i], traj_idx[i+1])].compute()

# The same `sst` variable can be retrieved by using the drifter's ID:

id_ex = ds.ID[i].values  # id of the i+1 th trajectory as an example
id_ex

j = int(np.where(ds.ID == id_ex)[0])  # retrieve back the index
ds.sst[slice(traj_idx[j], traj_idx[j+1])].compute()

# Once we know the indices of the trajectory of interest, we can calculate statistics like `mean()` or other reducing operations on one, or a list of variables:

s_var = ['ve', 'vn', 'gap', 'err_lat', 'err_lon', 'sst', 'sst1', 'sst2', 'err_sst', 'err_sst1', 'err_sst2']
ds.isel({'obs': slice(traj_idx[i], traj_idx[i+1]), 'traj': i})[s_var].mean().compute()

# ### Operations per trajectory

# As previously noted, to perform the same operation per trajectory, it is more efficient to align the *chunks* with the trajectories. This is done by settings the size of the *chunks* equal to the dimensions of the trajectories. However, here we need to know the lengths of all the trajectories in the order they are arranged in the ragged array *before* actually loading the dataset with *xarray*. This is clearly not practical as *xarray* does not provide an obvious mechanism to align the data chunks with specified indices.

rowsize = np.zeros(len(files), dtype='int')
for i, file in enumerate(files):
    with xr.open_dataset(file, decode_times=False) as ds_t:
        rowsize[i] = ds_t.sizes['obs']

# +
ds.close()  # close previously loaded xr.Dataset

# align chunks of the dask array with the length of each individual trajectory
chunk_settings = {'obs': tuple(rowsize.tolist())}

ds = xr.open_dataset('data/gdp_subset.nc', chunks=chunk_settings)
# -

# Variables such as the longitude, are now split into `subset_nb_drifters` chunks which have different sizes and where the maximum size is indicated by the `Shape` characteristic of the *xarray.DataArray* objects. As an example for `longitude`:

ds.longitude

# Naturally, now loading a trajectory always require loading *only* one chunk.

i = 10
ds.longitude.isel({'obs': slice(traj_idx[i], traj_idx[i+1])})


# #### Simple operation by chunks (or blocks)
#
# To perform arbitrary operation per trajectory, we can now use `map_blocks()` that applies a function per chunk (*block* is also used for *chunks*). In the example below we simply define the function `func` that calculates the mean of each block of an array `x`. Note that this requires loading `nb_subset_drifters` chunks and applying the operation.

# +
# %%time
def func(x):
    return np.array([np.nanmean(x)])

stats_traj = ds.sst.data.map_blocks(func).compute() # apply to sst variable
# -

stats_traj[:10]


# #### More complex operation where dimensions can change between input and output
#
# Alternatively, one can use the *xarray* function `apply_ufunc` to map a function per chunks. In this case, the function to be applied can be a bit more complex, but this method gives more flexibility to handle the input and output formats and dimensions of the function.
#
# In a first example, the eastward velocity is passed as an argument by chunk to the function which will calculate the anomaly per trajectory. The length of the output will be of the same length as the input. Please note here that:
#
# 1. The input and output sizes are not modified.
# 2. An argument must be passed to the function. It shouldn't be `ds.ve` (the xarray DataArray), but the `ds.ve.data` (the underlying dask core data array) must be used.

def per_chunk_anomaly(array):
    # MUST return an array (https://github.com/dask/dask/issues/8822)
    return array.map_blocks(lambda x: x-np.nanmean(x), chunks=array.chunks)


# +
# %%time

# here the apply_ufunc functions takes the function just defined above(per_chunk_anomaly)
# and the data to which apply that function
ret = xr.apply_ufunc(
    per_chunk_anomaly,
    ds.ve.data,  # .data to retrieve the underlying chunked dask array
    input_core_dims=[['obs']],
    output_core_dims=[['obs']],
    dask='allowed'
).compute()
# -

# And display some results:

display(ret)  # only a few values will be shown by default
display(len(ret))  # length of the output should be same as length of input


# In a second example, we calculates `mean()` values per trajectory. This means that for our datasets consisting of `nb_subset_drifters` chunks, ttput will have `nb_subset_drifters` values, that is one value per chunk. In other words, the length of the output will be different from the length of the input.

def per_chunk_mean(array):
    nchunks = len(array.chunks[0])
    output_chunks = ([1] * nchunks,) # 1 value per chunk
    return array.map_blocks(lambda x: np.nanmean(x, keepdims=True), chunks=output_chunks)


# +
# %%time

ret = xr.apply_ufunc(
    per_chunk_mean,
    ds.ve.data,
    input_core_dims=[['obs']],  # input dimension to the per_block function
    output_core_dims=[['obs']], # output still has one dimension
    exclude_dims=set(['obs']),  # size of x changes so it has to be in the exclude_dims param
    dask='allowed',
).compute()
# -

# And display some results:

display(ret[:10])  # show only first 10 values
display(len(ret))  # length of output should be the number of trajectories

# + [markdown] tags=[]
# In a last example, we estimate ocean velocity rotary spectra of the complex-valued time series `u+vi` via the periodogram method (and using the *NumPy* `fft` function). Here, the combination of the two methods `apply_ufunc` and `map_blocks` is a powerful tool which can serve as templates for a range of advanced processing applied per trajectory.
#
# First, we create the new complex-valued variable `cv` which inherits the chunks from `ve` and `vn`:
# -

ds = ds.assign(cv = ds['ve'] + 1j*ds['vn'])
ds.cv


def per_chunk_periodogram(array):
    dt = 1/24  # [-]
    return array.map_blocks(lambda x: dt*np.abs(np.fft.fft(x))**2, chunks=array.chunks)


# Here we benchmark this last, more complex, operation:

# +
t0 = time.time()

ret = xr.apply_ufunc(
    per_chunk_periodogram,
    ds['cv'].data,
    input_core_dims=[["obs"]],  # input dimension to the per_block function
    output_core_dims=[["obs"]],  # output still has one dimension
    dask='allowed'
).compute()

benchmark_times[0,2] = time.time() - t0
# -

# The return variable is the same length as `ds['cv']`, and is a ragged array of estimated rotary spectra by the periodogram method.
#
# (Please note: the periodogram is not a good spectral estimator at all and alternative methods such as multitaper methods should be used to estimate spectra. Please also note that we assumed that the individual trajectories were gap-free at regular hourly intervals which is required to apply a FFT. However, some velocity time series have gaps, in which case the FFT calculation is not valid)

# Display one example spectrum:

i = 0   # drifter index

# +
# calculate inertial frequency in cycle per day [cpd] from the mean latitude of trajectory
omega = 7.2921159e-5  # Earth's rotation rate [rad/s]
seconds_per_day = 60*60*24  # [s]
fi = -2*omega*(seconds_per_day/(2*np.pi))*np.sin(np.radians(ds.latitude[traj_idx[i]:traj_idx[i+1]]).mean().compute())

# define frequency scale/abscissa
dt = 1/24  # [-]
f = np.fft.fftfreq(int(ds.rowsize[i].compute()), dt) 
ss = np.log10(ret[traj_idx[i]:traj_idx[i+1]])  # spectrum of the ith trajectory 

fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1)

h1, = ax.plot(np.fft.fftshift(f), np.fft.fftshift(ss), scaley=True, label='Spectrum', linewidth=0.5)
h2 = ax.axvline(x=fi,color='k',linestyle=':', label='Inertial frequency', linewidth=0.5)
ax.legend(frameon=False)
ax.set_ylabel('PSD (m$^2$ s$^{-2}$ cpd$^{-1}$)')
ax.set_xlabel('Frequency [cpd]');

# + [markdown] tags=[]
# At this stage it is necessary to *clear the memory (RAM)* of the *Python* process because in the next step, the data are fully loaded in memory by using Pandas.

# + tags=[]
del ds, ds_subset, ret, traj_idx, stats_traj, rowsize, x_c, y_c

# + [markdown] tags=[]
# # *Pandas*
#
# In this section, we test the use of the *Pandas* package for our Lagrangian data. Since the previously-created NetCDF file containing the ragged array has two dimensions `['traj']` and `['obs']`, it cannot be read directly into the table structure of a `pandas.DataFrame()`. As a workaround, we load the data with *xarray*, drop the `['traj']` dimension, and convert the resulting data to a `pandas.DataFrame()`. The disadvantage is that it requires to form a second dataset with the dimension`['traj']` to have access to all variables (not presented here).
# -

# %%time
df = xr.open_dataset('data/gdp_subset.nc').drop_dims('traj').to_pandas()  # only contains the variables with dimension ['obs']

# In this case, the data is organized in a table format where each variable is associated with a column, and each row contains one observation. A *DataFrame* is easy to quickly look at, with the `.head()`, `.tail()` functions as an example:

df.head()

print(f'This subset contains {len(np.unique(df.ids))} drifters and {len(df):,} observations.')

# ## *Pandas* test 1: Geographical binning of any variable
# Here we reconduct the first bench test: calculate the mean zonal velocity from all drifters of the dataset.

# +
t0 = time.time()

lon = np.linspace(-180, 180, 360*2)
lat = np.linspace(-90, 90, 180*2)

ret = stats.binned_statistic_2d(df.longitude, 
                                df.latitude, 
                                df.ve,
                                statistic=np.nanmean, # can pass any function()
                                bins=[lon, lat])

benchmark_times[1,0] = time.time() - t0

# +
x_c = np.convolve(lon, [0.5, 0.5], mode='valid')
y_c = np.convolve(lat, [0.5, 0.5], mode='valid')

# get 1st and 99th percentiles of values to plot to get a useful range for the colorscale
v1,v2 = np.nanpercentile(ret.statistic.T,[1,99])

fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.Robinson(central_longitude=-180))
cmap = cmocean.tools.crop(cmocean.cm.balance, vmin=v1, vmax=v2, pivot=0)
pcm = ax.pcolormesh(x_c, y_c, 
                    ret.statistic.T, 
                    cmap=cmap, 
                    transform=ccrs.PlateCarree(),
                    vmin=v1, vmax=v2)

# gridlines and labels
gl = ax.gridlines(color='k', linewidth=0.1, linestyle='-',
                  xlocs=np.arange(-180, 181, 60), ylocs=np.arange(-90, 91, 30),
                  draw_labels=True)
gl.top_labels = False
gl.right_labels = False
# add land and coastline
ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05, axes_class=plt.Axes)
cb = fig.colorbar(pcm, cax=cax);
cb.ax.set_ylabel('Zonal velocity [m/s]');


# -

# ## *Pandas* test 2: Extract a given region
#
# The extraction of a region is slightly simpler with *Pandas* than with *xarray*, because the same mask can be applied to all variables of interest that share the `obs` dimension.

def retrieve_region_pd(df, lon: list = None, lat: list = None, time: list = None):
    '''Subset the dataset for a region in space and time
    
    Args:
        df: Pandas DataFrame
        lon: longitude slice of the subregion
        lat: latitude slice of the subregion
        time: tiem slice of the subregion
    
    Returns: 
        ds_subset: Dataset of the subregion
    '''
    mask = functools.reduce(np.logical_and, 
                            (
                                df.longitude > lon[0], 
                                df.longitude < lon[1],
                                df.latitude > lat[0],
                                df.latitude < lat[1],
                                df.time > day0,
                                df.time < day1,
                            )
                           )
    
    return df.loc[mask]


# +
t0 = time.time()

lon = [-98, -78]
lat = [18, 31]
day0 = datetime(2000,1,1)
day1 = datetime(2020,12,31)
days = [day0, day1]
df_subset = retrieve_region_pd(df, lon, lat, days)

benchmark_times[1,1] = time.time() - t0
# -

df_subset.head()

# Here we plot the result as before but displaying the speed for each data point:

# +
fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())

pcm = ax.scatter(df_subset.longitude, df_subset.latitude, 
               s=0.05, c=np.sqrt(df_subset.ve**2+df_subset.vn**2), transform=ccrs.PlateCarree(),
               cmap=cmocean.cm.speed)

ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
ax.set_xticks(np.arange(-95, -79, 5), crs=ccrs.PlateCarree())
ax.set_yticks([20, 25, 30], crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='3%', pad=0.02, axes_class=plt.Axes)
cb = fig.colorbar(pcm, cax=cax)
cb.set_label('Velocity magnitude [m/s]')
# -

# ## *Pandas* test 3: Single statistic per trajectory

# Single operation per trajectory can be easily implemented in a *Pandas DataFrame* by locating the drifter ID by index (`iloc`) or by value (`loc`).

i = 10  # drifter index

df.iloc[np.where(df['ids'] == np.unique(df['ids'])[i])].mean(numeric_only=False)

# Assuming we know a drifter ID `id_ex` (here we simply use the value associated to the i<sup>th</sup> index above), we can retrieve the associated data by value as follow.

id_ex = np.unique(df['ids'])[i]
id_ex

df.loc[df['ids'] == id_ex].mean(numeric_only=False)

# For more complicated operations per trajectory, the pandas `groupby()` function allows us to split the `DataFrame`. Applied to the `ids['obs']` (which repeat the ID of a drifter for each of its observations), we can obtain a *grouped object* containing one trajectory per group. Following this operation, one can apply a predefined set of operations, such as `mean()`, or any user defined functions using `.apply()`. As before, we provide an example where we can calculate the mean of SST per trajectory, and another example of estimating velocity spectra by the periodogram method.

# %%time
ret = df.groupby("ids").sst.mean()
ret

# Again, to estimate the velocity spectra we have to create the new complex-valued variable `cv` from `ve` and `vn`:

df['cv'] = df['ve'] + 1j*df['vn']


# And calculate the periodogram per trajectory using this new variable:

def periodogram_per_group(array):
    dt = 1/24
    return dt*np.abs(np.fft.fft(array))**2


# +
t0 = time.time()

ret = df.groupby("ids").cv.apply(periodogram_per_group)

benchmark_times[1,2] = time.time() - t0
# -

# This time, the results are stored into a *dictionary* where the keys are the drifters' ID:

ret

# As an example, we display the first 10 values of the sprctrum for drifter `id_ex`:

ret[id_ex][:10]

del df, df_subset, ret, x_c, y_c  # again free the memory before the next section

# + [markdown] tags=[]
# # *Awkward Array*
# [*Awkward Array*](https://awkward-array.readthedocs.io/en/latest/) is a library for nested, variable-sized data, including arbitrary-length lists, records, mixed types, and missing data, using NumPy-like idioms. Such arrays are dynamically typed (defined at runtime as a function of the variable to store), but operations on them are compiled into *machine code* and therefore executes faster than regular *interpreted* *Python* function. This allow to generalizes *NumPy* array manipulation routines, even with variable-sized data.
#
# A schematic view of the data structure is presented in the figure below. The higher level `ak.Array` and `ak.Record` hides the nested structure of the data structure, but can always be accessed with `ak.Array.layout` (or `ds_ak.layout` in our case). This structure also stores parameters or metadata such as *units*, *long name*, etc. associated with the data. The library stores data into standard `NumPyArray` alongside a `ListOffsetArray` for fast and efficient access to variables, even with nonuniform data length.
#
# <div>
# <img src="https://i.imgur.com/HogZmOH.png" width="800"/>
# </div>
#
# The main advantages of Awkward Array are:
# - the indexing is already taken care of by the library, e.g. `sst[400]` returns the sea surface temperature along the 401<sup>st</sup> trajectory;
# - ability to efficiently perform operations per trajectory;
# - easy integration with Numba (demonstrated below in section 7.4).
#
# An Awkward array can easily be created by reading our NetCDF file:
# -

ds_ak = create_ak(xr.open_dataset('data/gdp_subset.nc', decode_times=False))

# *Awkward Arrays* supports N-dimensional datasets by storing nested arrays. The main dataset contains variables `(type = subset_nb_drifters * {various type})` containing the metadata.

ds_ak

# *Awkward Array* doesn't (yet!) have an *html* representation of its structure, but it is possible to list the fields. 

ds_ak.fields  # list of fields/variables

# If we peak inside one of the field (or variable), we can see the associated `type`. For example, the drifters' ID have a `type=subset_nb_drifters * int64`.

ds_ak.ID  # one variable

# If we display the last field 'obs', we can see that it is a nested *Awkward Array* and contains all variables with `type=(subset_nb_drifters * var * dtype)` containing data along trajectories.

ds_ak.obs

# The library includes the function `ak.flatten()`, similar to `np.flatten()` to concatenate all observations for one variable into a unidimensional array. As an example, with 'sst':

# + tags=[]
print(f'Total length of the data inside \'obs\' field \'sst\' are {len(ak.flatten(ds_ak.obs.sst)):,}.')
ak.flatten(ds_ak.obs.sst)

# + [markdown] tags=[]
# A nested structure is utilized to efficiently store N-dimensional dataset, in our case we first have the fields with dimension `['traj']`, followed by the fields with dimension `['obs']` stored inside the array `ds_ak.obs`.
# -

ds_ak.obs.fields

# For example, the type of the `sst` field, stored at `ds_ak.obs.sst`, is `17324 * var * float32`. This means that there are 17324 trajectories of var*iable* size of float32`.

ds_ak.obs.sst

# The data along the trajectory of a specific drifter can easily be retrieved using an index.

i = 0
ds_ak.obs.sst[i]

# The same data can be extracted from the drifter ID:

id_ex = ds_ak.ID[i] # id of the ith trajectory as an example
display(id_ex)
i = np.where(ds_ak.ID == id_ex)[0][0]
ds_ak.obs.sst[i]

# And the data along a specific trajectory can be accessed using a second index. As an example, the first sst value of the `i`<sup>th</sup> trajectory:

ds_ak.obs.sst[i][0]  # [K]

# *Metadata* or *attributes* are store for the global Array `ds_ak.layout.parameters`, as well as for each individual variable (`ds_ak.obs.sst.layout.parameters`), similarly to global attributes and variable attributes in a NetCDF file. Those attributes are stored as a parameter in the `ak.RecordArray` (obtained with the `.layout` member), which summarizes the data fields, the types, and the shapes of the data itself.

ds_ak.layout.parameters

ds_ak.layout.parameters

ds_ak.obs.sst.layout.parameters

# + [markdown] tags=[]
# ## *Awkward Array* test 1: Geographical binning of any variable
# Again, we reconduct the first bench test: calculate the mean zonal velocity from all drifters of the dataset. For operations apply on the full dataset, we use the `ak.flatten()` function to retrieve the underlying unidimensional *NumPy* array containing all the observations for all drifters.

# +
t0 = time.time()

# can we save the processing time(s) as a variable to later compare to other formats?
lon = np.linspace(-180, 180, 360 * 2)
lat = np.linspace(-90, 90, 180 * 2)

ret = stats.binned_statistic_2d(ak.flatten(ds_ak.obs.longitude, axis=1), 
                                ak.flatten(ds_ak.obs.latitude, axis=1), 
                                ak.flatten(ds_ak.obs.ve, axis=1),
                                statistic=np.nanmean,
                                bins=[lon, lat])
        
benchmark_times[2,0] = time.time() - t0

# +
x_c = np.convolve(lon, [0.5, 0.5], mode='valid')
y_c = np.convolve(lat, [0.5, 0.5], mode='valid')

# get 1st and 99th percentiles of values to plot to get a useful range for the colorscale
v1,v2 = np.nanpercentile(ret.statistic.T,[1,99])

fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.Robinson(central_longitude=-180))
cmap = cmocean.tools.crop(cmocean.cm.balance, vmin=v1, vmax=v2, pivot=0)
pcm = ax.pcolormesh(x_c, y_c, 
                    ret.statistic.T, 
                    cmap=cmap, 
                    transform=ccrs.PlateCarree(),
                    vmin=v1, vmax=v2)

# gridlines and labels
gl = ax.gridlines(color='k', linewidth=0.1, linestyle='-',
                  xlocs=np.arange(-180, 181, 60), ylocs=np.arange(-90, 91, 30),
                  draw_labels=True)
gl.top_labels = False
gl.right_labels = False
# add land and coastline
ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05, axes_class=plt.Axes)
cb = fig.colorbar(pcm, cax=cax);
cb.ax.set_ylabel('Zonal velocity [m/s]');


# -

# ## *Awkward Array* test 2: Extract a given region
#
# With *Awkward Array*, the extraction of a subregion is slightly more complex than with *Pandas*, since here the dataset contains both variables with dimension `['traj']` and variables with dimension `['obs']`. Note that comparisons can be performed on the bidimensional non-regular `ak.Array` (e.g. `ds.obs.longitude`, `ds.obs.latitude`, `ds.obs.time`) without looping.

def retrieve_region_ak(ds: ak.Array, lon: list = None, lat: list = None, days: list = None) -> ak.Array:
    '''Subset the dataset for a region in space and time
    
    Args:
        ds: Awkward Array
        lon: longitude slice of the subregion
        lat: latitude slice of the subregion
        days: days slice of the subregion
    
    Returns: 
        ds_subset: Dataset of the subregion
    '''
    mask = functools.reduce(np.logical_and, 
                            (
                                ds.obs.longitude > lon[0], 
                                ds.obs.longitude < lon[1],
                                ds.obs.latitude > lat[0],
                                ds.obs.latitude < lat[1],
                                ds.obs.time > days[0],
                                ds.obs.time < days[1],
                            )
                           )
    
    ds_s = ak.copy(ds)
    mask_id = np.in1d(ds_s.ID, np.unique(ak.flatten(ds_s.obs.ids[mask])))
    ds_s = ds_s[mask_id]  # mask for variables with dimension ['traj']
    ds_s.obs = ds_s.obs[mask[mask_id]] # mask for variables with dimension ['obs']
    
    return ds_s


# +
t0 = time.time()

lon = [-98, -78]
lat = [18, 31]
day0 = (datetime(2000,1,1) - datetime(1970,1,1)).total_seconds()
day1 = (datetime(2020,12,31) - datetime(1970,1,1)).total_seconds()
days = [day0, day1]
ds_subset = retrieve_region_ak(ds_ak, lon, lat, days)

benchmark_times[2,1] = time.time() - t0
# -

# Here we plot the result as before but displaying the drogue status of drifters along their trajectory. *Note: the drogue is a sea anchor centered at 15 m depth that can become detached, after which the drifter is more strongly affected by surface winds and waves.*

# +
fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())

cond = ds_subset.obs.drogue_status  # True: drogued, False: undrogued
pcm = ax.scatter(ak.flatten(ds_subset.obs.longitude[cond]), ak.flatten(ds_subset.obs.latitude[cond]), 
               s=0.05, c='violet', transform=ccrs.PlateCarree(), label='Drogued')

pcm = ax.scatter(ak.flatten(ds_subset.obs.longitude[~cond]), ak.flatten(ds_subset.obs.latitude[~cond]), 
               s=0.05, c='c', transform=ccrs.PlateCarree(), label='Undrogued')

ax.add_feature(cfeature.LAND, facecolor='grey', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.25, zorder=1)
ax.set_xticks(np.arange(-95, -79, 5), crs=ccrs.PlateCarree())
ax.set_yticks([20, 25, 30], crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('Drogue status of each observation', size=8);
ax.legend(markerscale=20, labelcolor='w', frameon=False);
# -

# ## *Awkward Array* test 3: Single statistic per trajectory

# Without the need for indices, we can perform reduction operation per trajectory directly with Awkward array, which simplify considerably the notations, and should ease the development of new functionality.
#
# *Note*: At this point, the dataset `ds_ak` is loaded in memory, which explains the speed of the operations. For larger dataset that cannot be held completely in memory, an option could be to interface with [Dask](https://dask.org), currently under development.

# +
# %%time

avg_sst = np.zeros(len(ds_ak.obs))
for i, s in enumerate(ds_ak.obs.sst):
    avg_sst[i] = np.nanmean(s)
avg_sst[:10]
# -

# For basic operations, we can also use *Awkward Array* to perform averages along a specific axis. In our situation, `ak.mean(longitude, axis=1)` perform the same mean operation per trajectory, see that the type is then reduced to `subset_nb_drifters * float64`.
#
# *Note: The `nan` versions of those operations (`ak.nanmean`, `ak.nanstd`, `ak.nanmax`, etc.) is not yet available but is currently in development.

avg_lon = ak.mean(ds_ak.obs.longitude, axis=1)
avg_lon


# Applying more complex operation can be easily implemented with simple `for-loop`, since the indexing is taken care by *Awkward Array*.

def periodogram_per_traj(uv):
    dt = 1/24
    d = []    
    for i in range(0, len(uv)):
        d.append(dt*np.abs(np.fft.fft(uv[i]))**2)
    return d


# +
t0 = time.time()

ret = periodogram_per_traj(
    ds_ak.obs.ve + 1j*ds_ak.obs.vn
)

benchmark_times[2,2] = time.time() - t0
# -

# Each element of the list `ret` now contains the fast Fourier transform of the complex velocity `u + iv` per trajectory:

ret[:5]


# ## Numba

# *Awkward Array* can be combined with [Numba](https://numba.pydata.org) to accelerate calculations. Here, the goal is *not* to show the most efficient way of performing a calculation, but to present how simply adding the numba decorator `@nb.njit` to a function can improved the performance by order of magnitude(s).
#
# Here we show an example that calculates the kinetic energy of a drifter trajectory from its velocity time series:

# +
def kinetic_energy(u, v):
    ke = np.zeros(len(u))
    for i in range(0, len(u)):
        ke[i] = np.sqrt(u[i]**2 + v[i]**2)
    return ke
        
@nb.njit
def kinetic_energy_nb(u, v):
    ke = np.zeros(len(u))
    for i in range(0, len(u)):
        ke[i] = np.sqrt(u[i]**2 + v[i]**2)
    return ke


# -

# select a random trajectory
i = 10

# %%time
ke = kinetic_energy(ds_ak.obs.ve[i], ds_ak.obs.vn[i])

# The function is compiled just in time when we execute the function for the first time, future executions are *numba fast*.

kinetic_energy_nb(ds_ak.obs.ve[i], ds_ak.obs.vn[i])

# %%timeit -r10 -n10
ke2 = kinetic_energy_nb(ds_ak.obs.ve[i], ds_ak.obs.vn[i])

# This results in more than a 500x sped up (!) for the same function simply by adding the `@nb.njit` decorators!

del ds_ak, ret, x_c, y_c

# # Discussion

# We presented a commonly used Lagrangian oceanographic dataset (the GDP dataset) which is currently available as individual NetCDF files (one of the means of distribution). Next, we presented an efficient data structure, the contiguous ragged array, to combine the variables from these individual NetCDF files. We then compared three different packages–*xarray*, *Pandas*, and *Awkward Array*—by performing typical Lagrangian workflow tasks.
#
# **Xarray**
#
# *xarray* is a well-known and established package used to perform operations on N-Dimensional datasets. It is natively integrated with *Dask* for parallel computing(not demonstrated in this Notebook), and allows users to *lazy load* data when the dataset is larger than the available memory of the computing environment. 
#
# However, it is not typically used with contiguous ragged array, so applying operation per trajectory requires to manually index through the dataset. One possibility is to set the size of the *Dask* *chunks* equals to the size of the trajectories, which allows for mapping operation in parallel per trajectory. However, the typical high number of chunks is less than ideal: it hinders performance since a simple operation like computing mean values across a dataset containing *n* trajectories requires to conduct *n* reading operation on the data file.
#
# **Pandas**
#
# Pandas is a predominantly used *Python* data analysis package. Since it is designed to perform operations on tabular data, it is required to form two *DataFrame* tables to represent the complete GDP dataset: one containing the variables with one value per trajectory (`['traj']`), and a second one containing the variables with one value per observations along the trajectory (`['obs']`). Unfortunately, this creates a separation the data and their metadata.
#
# In this Notebook we used only a subset of the GDP dataset by randomly selecting only 500 trajectories. The data were therefore entirely contained within the active memory and the operations performed were *fast* and written in an elegant and intuitive fashion. However, if these operations are conducted on the entire dataset (17324 trajectories) we found the execution to be much slower than with *xarray* or *Awkward Array* which seem able to manage memory much more efficiently. 
#
# **Awkward Array**
#
# *Awkward Array* is a novel library specifically designed to deal with ragged and heterogeneous data (in type or size). With the example of the heterogeneous GDP dataset, we find that this library simplifies considerably Lagrangian analysis. Furthermore, integration with *Numba* allows to speed up calculations without major redesign. We anticipate that these two advantages will lead to faster development of Lagrangian analysis functions as part of the *CloudDrift* project.
#
# Initially developed for particle physics applications, *Awkward Array* is missing some useful features (e.g. *html* representation, import from *NetCDF*, and especially *Dask* integration) when compared to more mature libraries like *xarray* or *Pandas*. During the development of this Notebook, we had the opportunity to engage with the authors of this library, and we plan on collaborating to fill those gaps during the development the *clouddrift* libraries. We believe that this collaboration will elevate both projects, which are sponsored by the National Science Foundation during similar time frame (*Awkward Array* [#2103945](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2103945)).

# ## Benchmark speed

# The following figure presents the benchmark times obtain for the current execution. As a comparison, we include a reference time (red dashed line) obtained on a 2021 Mac Mini with a 8 cores Apple M1 ARM processor, 16GB of RAM, running macOS Monterey 12.3.

ref_times = np.array([[3.26, 0.46, 0.23],  # [s]
                      [3.21, 0.06, 0.38],
                      [3.22, 0.13, 0.32]])

# +
fig = plt.figure(dpi=150)
ax = fig.add_subplot(1,1,1)

index = np.arange(0,3)
bar_width = 0.2

t1 = plt.bar(index, benchmark_times[0,:], bar_width,
                 color='violet',
                 label='Xarray')

t2 = plt.bar(index + bar_width, benchmark_times[1,:], bar_width,
                 color='limegreen',
                 label='Pandas')

t3 = plt.bar(index + 2*bar_width, benchmark_times[2,:], bar_width,
                 color='aqua',
                 label='Awkward Array')

# add reference times
for i in range(0, len(index)):
    x = np.array([index[i], index[i] + bar_width, index[i] + 2*bar_width])
    ax.plot(x, ref_times[:,i], 'k', linewidth=0.75, linestyle='dashed', label='Reference time (Apple M1, 16GB)')

plt.xlabel('Workflow tests')
plt.ylabel('Elapsed time [s] (lower is better)')
plt.title('Benchmark times per library')
plt.xticks(index + bar_width, ('Binning', 'Region extraction', 'Periodogram per trajectory'))
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), frameon=False)


# + [markdown] tags=[]
# ## Feedback
# -

# <div>
# <img src="https://jeffcoespa.org/wp-content/uploads/2020/01/bigstock-We-Want-Your-Feedback-Promotio-321303232-768x591.jpg" width="400"/>
# </div>
#
# If you ran this notebook on a local computer, please help us guide the development of *CloudDrift* by sharing one or all following points to the discussion thread on [Github Discussion](https://github.com/Cloud-Drift/earthcube-meeting-2022/discussions/13):
# 1. your comments on the ease of use of Xarray and/or Pandas and/or Awkward Arrays for Lagrangian data analysis;
# 2. the figure of your benchmark timings in the previous cell;
# 2. your system information generated by executing the next cell;
# 4. any other comments!
#
# Thanks!

# +
# summary of the system for log purpose
# inspired from https://stackoverflow.com/a/58420504/1558320
def getSystemInfo():
    info={}
    info['platform']=platform.system()
    info['platform-release']=platform.release()
    info['platform-version']=platform.version()
    info['architecture']=platform.machine()
    info['processor']=platform.processor()
    try:
        info['frequency']=psutil.cpu_freq(percpu=False)
    except:
        info['frequency']='N/A'
    info['cores']=psutil.cpu_count(logical=False)
    info['threads']=psutil.cpu_count(logical=True)
    info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    return info

getSystemInfo()
# -

# ## Future development

# We hope you will follow the development of [CloudDrift](https://github.com/Cloud-Drift), and encourage everyone to share this Notebook as well as submit feedback and comments to team members.

# + [markdown] tags=[]
# # References
# - Elipot et al. (2016), "A global surface drifter dataset at hourly resolution", J. Geophys. Res. Oceans, 121, [doi:10.1002/2016JC011716](https://doi.org/10.1002/2016JC011716)
# - Hansen, D. V., & Poulain, P. M. (1996). Quality control and interpolations of WOCE-TOGA drifter data. Journal of Atmospheric and Oceanic Technology, 13(4), 900-909, [doi:10.1175/1520-0426(1996)013%3C0900:QCAIOW%3E2.0.CO;2](http://dx.doi.org/10.1175/1520-0426(1996)013<0900:QCAIOW>2.0.CO;2)
