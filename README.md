[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Cloud-Drift/earthcube-meeting-2022/main?labpath=PM_05_Accelerating_Lagrangian_analyses_of_oceanic_data_benchmarking_typical_workflows.ipynb)

# 2022 EarthCube Annual meeting

## Accelerating Lagrangian analyses of oceanic data: benchmarking typical workflows

[Philippe Miron](https://github.com/philippemiron)<sup>1</sup>, [Shane Elipot](https://github.com/selipot)<sup>2</sup>, [Rick Lumpkin](https://github.com/RickLumpkin)<sup>3</sup>, [Bertrand Dano](https://github.com/bdano63)<sup>2</sup>

- <sup>1</sup> Florida State University, USA
- <sup>2</sup> University of Miami, USA
- <sup>3</sup> NOAA’s Atlantic Oceanographic and Meteorological Laboratory, USA

For data, “Lagrangian” refers to oceanic and atmosphere information acquired by observing platforms drifting with the flow they are embedded within, but also more broadly refers to the data originating from uncrewed platforms, vehicles, and animals that gather data along their unrestricted but complicated paths. Because such paths traverse both spatial and temporal dimensions, Lagrangian data often convolve spatial and temporal information that cannot always and readily be organized, cataloged, and stored in common data structures and file formats with the help of common libraries and standards. As such, for both data generators and data users, Lagrangian data present challenges that the CloudDrift project aims to overcome.

This [Notebook](https://github.com/Cloud-Drift/earthcube-meeting-2022/blob/main/PM_05_Accelerating_Lagrangian_analyses_of_oceanic_data_benchmarking_typical_workflows.ipynb), consists of systematic comparisons and evaluations of workflows for Lagrangian data, using as a basis the velocity and sea surface temperature dataset emanating from the drifting buoys of the Global Drifter Program. Specifically, we consider the interplay between diverse storage file formats (NetCDF, Parquet) and the data structure associated with common existing libraries in Python (xarray, pandas, and awkward) in order to test their adequacies for performing three common Lagrangian tasks:
1. binning of a variable on an Eulerian grid (e.g. mean temperature map);
2. extracting data within given geographical and/or temporal windows;
3. analyses per trajectory (e.g. single statistics, Fast Fourier Transforms).

Because the CloudDrift project aims at accelerating the use of Lagrangian data for atmospheric, oceanic, and climate sciences, we hope that this notebook will incite the community of users to eventually test it on their own platform and thus provide us with feedback on its ease of use and the intuitiveness of the proposed methods and guide future developments.


### How to run the Notebook on your own computer ?

In a terminal window, clone and build the environment using [Anaconda](https://docs.conda.io/en/latest/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html), then launch jupyter lab:

```
git clone https://github.com/Cloud-Drift/earthcube-meeting-2022
cd earthcube-meeting-2022
conda env create -f environment.yml
conda activate earthcube
jupyter lab
```

The last command should open the jupyter lab interface in your web browser. Once completed, click on the Notebook `PM_05_Accelerating_Lagrangian_analyses_of_oceanic_data_benchmarking_typical_workflows.ipynb`, and start exploring!
