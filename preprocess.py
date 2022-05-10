import xarray as xr
import numpy as np
from datetime import datetime
import pandas as pd
import awkward as ak
from tqdm import tqdm


def decode_date(t):
    '''
    The date format is specified in 'seconds since 1970-01-01 00:00:00' but the missing values
    are stored as -1e+34 which is not supported by the default parsing mechanism in xarray

    This function returns replaced the missing valye by NaT and return a datetime object.
    :param t: date
    :return: datetime object
    '''
    if np.isscalar(t):
        if np.isclose(t, -1e+34) or np.isnan(t):
            return np.datetime64('NaT')
        else:
            return pd.to_datetime(t, unit='s', origin='unix')
    else:
        nat_index = np.logical_or(np.isclose(t, -1e+34), np.isnan(t))
        t[nat_index] = np.datetime64('NaT')
        return pd.to_datetime(t, unit='s', origin='unix')


def fill_values(var, default=np.nan):
    '''
    Change fill values (-1e+34, inf, -inf) in var array to value specified by default
    '''
    missing_value = np.logical_or(np.isclose(var, -1e+34), ~np.isfinite(var))
    if np.any(missing_value):
        var[missing_value] = default
    return var


def str_to_float(value, default=np.nan):
    '''
    :param value: string
    :return: bool
    '''
    try:
        fvalue = float(value)
        if np.isnan(fvalue):
            return default
        else:
            return fvalue
    except ValueError:
        return default


def cut_str(value, max_length):
    '''
    Cut a string to a specify lenth.
    :param value: string
           max_length: lenght of the output
    :return: string with max_length chars
    '''
    return value[:max_length]


def drogue_presence(lost_time, time):
    '''
    Create drogue status from the drogue lost time and the trajectory time
    :params lost_time: timestamp of the drogue loss (or NaT)
            time[obs]: observation time
    :return: bool[obs]: 1 drogued, 0 undrogued
    '''
    if pd.isnull(lost_time) or lost_time >= time[-1]:
        return np.ones_like(time, dtype='bool')
    else:
        return time < lost_time


class create_ragged_array:
    def __init__(self, files):
        self.files = files
        self.rowsize = self.number_of_observations(self.files)
        self.nb_traj = len(self.rowsize)
        self.nb_obs = np.sum(self.rowsize).astype('int')
        self.allocate_data(self.nb_traj, self.nb_obs)
        self.index_traj = np.insert(np.cumsum(self.rowsize), 0, 0)

        for i, file in tqdm(enumerate(self.files), total=len(self.files)):
            #print(f'{i+1}/{self.nb_traj} files processed', end='\r')
            self.fill_ragged_array(file, i, self.index_traj[i])

    def number_of_observations(self, files) -> np.array:
        '''
        Load files and get the size of the observations.
        '''
        rowsize = np.zeros(len(files), dtype='int')
        for i, file in enumerate(files):
            with xr.open_dataset(file, decode_times=False) as ds:
                rowsize[i] = ds.sizes['obs']
        return rowsize

    def allocate_data(self, nb_traj, nb_obs):
        '''
        Reserve the space for the total size of the array
        '''
        # metadata
        self.id = np.zeros(nb_traj, dtype='int64')
        self.location_type = np.zeros(nb_traj, dtype='bool') # 0 Argos, 1 GPS
        self.wmo = np.zeros(nb_traj, dtype='int32')
        self.expno = np.zeros(nb_traj, dtype='int32')
        self.deploy_date = np.zeros(nb_traj, dtype='datetime64[s]')
        self.deploy_lat = np.zeros(nb_traj, dtype='float32')
        self.deploy_lon = np.zeros(nb_traj, dtype='float32')
        self.end_date = np.zeros(nb_traj, dtype='datetime64[s]')
        self.end_lon = np.zeros(nb_traj, dtype='float32')
        self.end_lat = np.zeros(nb_traj, dtype='float32')
        self.drogue_lost_date = np.zeros(nb_traj, dtype='datetime64[s]')
        self.type_death = np.zeros(nb_traj, dtype='int8')
        self.type_buoy = np.chararray(nb_traj, itemsize=15)
        self.deployment_ship = np.chararray(nb_traj, itemsize=15)
        self.deployment_status = np.chararray(nb_traj, itemsize=15)
        self.buoy_type_manufacturer = np.chararray(nb_traj, itemsize=15)
        self.buoy_type_sensor_array = np.chararray(nb_traj, itemsize=15)
        self.current_program = np.zeros(nb_traj, dtype='int32')
        self.purchaser_funding = np.chararray(nb_traj, itemsize=15)
        self.sensor_upgrade = np.chararray(nb_traj, itemsize=15)
        self.transmissions = np.chararray(nb_traj, itemsize=15)
        self.deploying_country = np.chararray(nb_traj, itemsize=15)
        self.deployment_comments = np.chararray(nb_traj, itemsize=15)
        self.manufacture_year = np.zeros(nb_traj, dtype='int16')
        self.manufacture_month = np.zeros(nb_traj, dtype='int16')
        self.manufacture_sensor_type = np.chararray(nb_traj, itemsize=5)
        self.manufacture_voltage = np.zeros(nb_traj, dtype='int16')
        self.float_diameter = np.zeros(nb_traj, dtype='float32')
        self.subsfc_float_presence = np.zeros(nb_traj, dtype='bool')
        self.drogue_type = np.chararray(nb_traj, itemsize=15)
        self.drogue_length = np.zeros(nb_traj, dtype='float32')
        self.drogue_ballast = np.zeros(nb_traj, dtype='float32')
        self.drag_area_above_drogue = np.zeros(nb_traj, dtype='float32')
        self.drag_area_drogue = np.zeros(nb_traj, dtype='float32')
        self.drag_area_ratio = np.zeros(nb_traj, dtype='float32')
        self.drag_center_depth = np.zeros(nb_traj, dtype='float32')
        self.drogue_detect_sensor = np.chararray(nb_traj, itemsize=15)

        # values define at every observations (timesteps)
        self.longitude = np.zeros(nb_obs, dtype='float32')
        self.latitude = np.zeros(nb_obs, dtype='float32')
        self.time = np.zeros(nb_obs, dtype='datetime64[s]')
        self.ve = np.zeros(nb_obs, dtype='float32')
        self.vn = np.zeros(nb_obs, dtype='float32')
        self.err_lat = np.zeros(nb_obs, dtype='float32')
        self.err_lon = np.zeros(nb_obs, dtype='float32')
        self.err_ve = np.zeros(nb_obs, dtype='float32')
        self.err_vn = np.zeros(nb_obs, dtype='float32')
        self.gap = np.zeros(nb_obs, dtype='float32')
        self.drogue_status = np.zeros(nb_obs, dtype='bool') # 1 drogued, 0 undrogued

        # sst data set
        self.sst = np.zeros(nb_obs, dtype='float32')
        self.sst1 = np.zeros(nb_obs, dtype='float32')
        self.sst2 = np.zeros(nb_obs, dtype='float32')
        self.err_sst = np.zeros(nb_obs, dtype='float32')
        self.err_sst1 = np.zeros(nb_obs, dtype='float32')
        self.err_sst2 = np.zeros(nb_obs, dtype='float32')
        self.flg_sst = np.zeros(nb_obs, dtype='int8')
        self.flg_sst1 = np.zeros(nb_obs, dtype='int8')
        self.flg_sst2 = np.zeros(nb_obs, dtype='int8')

    def fill_ragged_array(self, file, tid, oid):
        '''
        Fill the ragged array from the xr.Dataset() corresponding to one trajectory

        Input filename: path and filename of the netCDF file
              tid: trajectory index
              oid: observation index in the ragged array
        '''
        ds = xr.open_dataset(file, decode_times=False)
        size = ds.dims['obs']

        # scalar
        self.id[tid] = int(ds.ID.data[0])
        self.wmo[tid] = ds.WMO.data[0]
        self.expno[tid] = ds.expno.data[0]
        self.deploy_date[tid] = decode_date(ds.deploy_date.data[0])
        self.deploy_lon[tid] = ds.deploy_lon.data[0]
        self.deploy_lat[tid] = ds.deploy_lat.data[0]
        self.end_date[tid] = decode_date(ds.end_date.data[0])
        self.end_lon[tid] = ds.end_lon.data[0]
        self.end_lat[tid] = ds.end_lat.data[0]
        self.drogue_lost_date[tid] = decode_date(ds.drogue_lost_date.data[0])
        self.type_death[tid] = ds.typedeath.data[0]
        self.type_buoy[tid] = ds.typebuoy.data[0]

        # vectors
        self.longitude[oid:oid+size] = ds.longitude.data[0]
        self.latitude[oid:oid+size] = ds.latitude.data[0]
        self.time[oid:oid+size] = decode_date(ds.time.data[0])
        self.ve[oid:oid+size] = ds.ve.data[0]
        self.vn[oid:oid+size] = ds.vn.data[0]
        self.err_lat[oid:oid+size] = ds.err_lat.data[0]
        self.err_lon[oid:oid+size] = ds.err_lon.data[0]
        self.err_ve[oid:oid+size] = ds.err_ve.data[0]
        self.err_vn[oid:oid+size] = ds.err_vn.data[0]
        self.gap[oid:oid+size] = ds.gap.data[0]
        self.sst[oid:oid+size] = fill_values(ds.sst.data[0])
        self.sst1[oid:oid+size] = fill_values(ds.sst1.data[0])
        self.sst2[oid:oid+size] = fill_values(ds.sst2.data[0])
        self.err_sst[oid:oid+size] = fill_values(ds.err_sst.data[0])
        self.err_sst1[oid:oid+size] = fill_values(ds.err_sst1.data[0])
        self.err_sst2[oid:oid+size] = fill_values(ds.err_sst2.data[0])
        self.flg_sst[oid:oid+size] = ds.flg_sst.data[0]
        self.flg_sst1[oid:oid+size] = ds.flg_sst1.data[0]
        self.flg_sst2[oid:oid+size] = ds.flg_sst2.data[0]
        self.drogue_status[oid:oid+size] = drogue_presence(self.drogue_lost_date[tid], self.time[oid:oid+size])

        # those values were store in the attributes
        self.location_type[tid] = 0 if ds.location_type == 'Argos' else 1  # 0 Argos, 1 GPS
        self.deployment_ship[tid] = cut_str(ds.DeployingShip, 15)
        self.deployment_status[tid] = cut_str(ds.DeploymentStatus, 15)
        self.buoy_type_manufacturer[tid] = cut_str(ds.BuoyTypeManufacturer, 15)
        self.buoy_type_sensor_array[tid] = cut_str(ds.BuoyTypeSensorArray, 15)
        self.current_program[tid] = str_to_float(ds.CurrentProgram, -1)
        self.purchaser_funding[tid] = cut_str(ds.PurchaserFunding, 15)
        self.sensor_upgrade[tid] = cut_str(ds.SensorUpgrade, 15)
        self.transmissions[tid] = cut_str(ds.Transmissions, 15)
        self.deploying_country[tid] = cut_str(ds.DeployingCountry, 15)
        self.deployment_comments[tid] = cut_str(ds.DeploymentComments.encode('ascii', 'ignore').decode('ascii'), 15) # remove not ascii char
        self.manufacture_year[tid] = str_to_float(ds.ManufactureYear, -1)
        self.manufacture_month[tid] = str_to_float(ds.ManufactureMonth, -1)
        self.manufacture_sensor_type[tid] = cut_str(ds.ManufactureSensorType, 15)
        self.manufacture_voltage[tid] = str_to_float(ds.ManufactureVoltage[:-6], -1) # e.g. 56 V
        self.float_diameter[tid] = str_to_float(ds.FloatDiameter[:-3]) # e.g. 35.5 cm
        self.subsfc_float_presence[tid] = str_to_float(ds.SubsfcFloatPresence)
        self.drogue_type[tid] = cut_str(ds.DrogueType, 7)
        self.drogue_length[tid] = str_to_float(ds.DrogueLength[:-2]) # e.g. 4.8 m
        self.drogue_ballast[tid] = str_to_float(ds.DrogueBallast[:-3]) # e.g. 1.4 kg
        self.drag_area_above_drogue[tid] = str_to_float(ds.DragAreaAboveDrogue[:-4]) # 10.66 m^2
        self.drag_area_drogue[tid] = str_to_float(ds.DragAreaOfDrogue[:-4]) # e.g. 416.6 m^2
        self.drag_area_ratio[tid] = str_to_float(ds.DragAreaRatio) # e.g. 39.08
        self.drag_center_depth[tid] = str_to_float(ds.DrogueCenterDepth[:-2]) # e.g. 15.0 m
        self.drogue_detect_sensor[tid] = cut_str(ds.DrogueDetectSensor, 15)

    def to_xarray(self):
        ds = xr.Dataset(
            data_vars=dict(
                rowsize=(['traj'], self.rowsize, {'long_name': 'Number of observations per trajectory', 'sample_dimension': 'obs', 'units':'-'}),
                location_type=(['traj'], self.location_type, {'long_name': 'Satellite-based location system', 'units':'-', 'comments':'0 (Argos), 1 (GPS)'}),
                WMO=(['traj'], self.wmo, {'long_name': 'World Meteorological Organization buoy identification number', 'units':'-'}),
                expno=(['traj'], self.expno, {'long_name': 'Experiment number', 'units':'-'}),
                deploy_date=(['traj'], self.deploy_date, {'long_name': 'Deployment date and time'}),
                deploy_lon=(['traj'], self.deploy_lon, {'long_name': 'Deployment longitude', 'units':'degrees_east'}),
                deploy_lat=(['traj'], self.deploy_lat, {'long_name': 'Deployment latitude', 'units':'degrees_north'}),
                end_date=(['traj'], self.end_date, {'long_name': 'End date and time'}),
                end_lat=(['traj'], self.end_lat, {'long_name': 'End latitude', 'units':'degrees_north'}),
                end_lon=(['traj'], self.end_lon, {'long_name': 'End longitude', 'units':'degrees_east'}),
                drogue_lost_date=(['traj'], self.drogue_lost_date, {'long_name': 'Date and time of drogue loss'}),
                type_death=(['traj'], self.type_death, {'long_name': 'Type of death', 'units':'-', 'comments': '0 (buoy still alive), 1 (buoy ran aground), 2 (picked up by vessel), 3 (stop transmitting), 4 (sporadic transmissions), 5 (bad batteries), 6 (inactive status)'}),
                type_buoy=(['traj'], self.type_buoy, {'long_name': 'Buoy type (see https://www.aoml.noaa.gov/phod/dac/dirall.html)', 'units':'-'}),
                DeploymentShip=(['traj'], self.deployment_ship, {'long_name': 'Name of deployment ship', 'units':'-'}),
                DeploymentStatus=(['traj'], self.deployment_status, {'long_name': 'Deployment status', 'units':'-'}),
                BuoyTypeManufacturer=(['traj'], self.buoy_type_manufacturer, {'long_name': 'Buoy type manufacturer', 'units':'-'}),
                BuoyTypeSensorArray=(['traj'], self.buoy_type_sensor_array, {'long_name': 'Buoy type sensor array', 'units':'-'}),
                CurrentProgram=(['traj'], self.current_program, {'long_name': 'Current Program', 'units':'-', '_FillValue': '-1'}),
                PurchaserFunding=(['traj'], self.purchaser_funding, {'long_name': 'Purchaser funding', 'units':'-'}),
                SensorUpgrade=(['traj'], self.sensor_upgrade, {'long_name': 'Sensor upgrade', 'units':'-'}),
                Transmissions=(['traj'], self.transmissions, {'long_name': 'Transmissions', 'units':'-'}),
                DeployingCountry=(['traj'], self.deploying_country, {'long_name': 'Deploying country', 'units':'-'}),
                DeploymentComments=(['traj'], self.deployment_comments, {'long_name': 'Deployment comments', 'units':'-'}),
                ManufactureYear=(['traj'], self.manufacture_year, {'long_name': 'Manufacture year', 'units':'-', '_FillValue': '-1'}),
                ManufactureMonth=(['traj'], self.manufacture_month, {'long_name': 'Manufacture month', 'units':'-', '_FillValue': '-1'}),
                ManufactureSensorType=(['traj'], self.manufacture_sensor_type, {'long_name': 'Manufacture Sensor Type', 'units':'-'}),
                ManufactureVoltage=(['traj'], self.manufacture_voltage, {'long_name': 'Manufacture voltage', 'units':'-', '_FillValue': '-1'}),
                FloatDiameter=(['traj'], self.float_diameter, {'long_name': 'Diameter of surface floater', 'units':'cm'}),
                SubsfcFloatPresence=(['traj'], self.subsfc_float_presence, {'long_name': 'Subsurface Float Presence', 'units':'-'}),
                DrogueType=(['traj'], self.type_buoy, {'drogue_type': 'Drogue Type', 'units':'-'}),
                DrogueLength=(['traj'], self.drogue_length, {'long_name': 'Length of drogue.', 'units':'m'}),
                DrogueBallast=(['traj'], self.drogue_ballast, {'long_name': "Weight of the drogue's ballast.", 'units':'kg'}),
                DragAreaAboveDrogue=(['traj'], self.drag_area_above_drogue, {'long_name': 'Drag area above drogue.', 'units':'m^2'}),
                DragAreaOfDrogue=(['traj'], self.drag_area_drogue, {'long_name': 'Drag area drogue.', 'units':'m^2'}),
                DragAreaRatio=(['traj'], self.drag_area_ratio, {'long_name': 'Drag area ratio', 'units':'m'}),
                DrogueCenterDepth=(['traj'], self.drag_center_depth, {'long_name': 'Average depth of the drogue.', 'units':'m'}),
                DrogueDetectSensor=(['traj'], self.drogue_detect_sensor, {'long_name': 'Drogue detection sensor', 'units':'-'}),

                # position and velocity
                ve=(['obs'], self.ve, {'long_name': 'Eastward velocity', 'units':'m/s'}),
                vn=(['obs'], self.vn, {'long_name': 'Northward velocity', 'units':'m/s'}),
                gap=(['obs'], self.gap, {'long_name': 'Time interval between previous and next location', 'units':'s'}),
                err_lat=(['obs'], self.err_lat, {'long_name': '95% confidence interval in latitude', 'units':'degrees_north'}),
                err_lon=(['obs'], self.err_lon, {'long_name': '95% confidence interval in longitude', 'units':'degrees_east'}),
                err_ve=(['obs'], self.err_ve, {'long_name': '95% confidence interval in eastward velocity', 'units':'m/s'}),
                err_vn=(['obs'], self.err_vn, {'long_name': '95% confidence interval in northward velocity', 'units':'m/s'}),
                drogue_status=(['obs'], self.drogue_status, {'long_name': 'Status indicating the presence of the drogue', 'units':'-', 'flag_values':'1,0', 'flag_meanings': 'drogued, undrogued'}),

                # sst
                sst=(['obs'], self.sst, {'long_name': 'Fitted sea water temperature', 'units':'Kelvin', 'comments': 'Estimated near-surface sea water temperature from drifting buoy measurements. It is the sum of the fitted near-surface non-diurnal sea water temperature and fitted diurnal sea water temperature anomaly. Discrepancies may occur because of rounding.'}),
                sst1=(['obs'], self.sst1, {'long_name': 'Fitted non-diurnal sea water temperature', 'units':'Kelvin', 'comments': 'Estimated near-surface non-diurnal sea water temperature from drifting buoy measurements'}),
                sst2=(['obs'], self.sst2, {'long_name': 'Fitted diurnal sea water temperature anomaly', 'units':'Kelvin', 'comments': 'Estimated near-surface diurnal sea water temperature anomaly from drifting buoy measurements'}),
                err_sst=(['obs'], self.err_sst, {'long_name': 'Standard uncertainty of fitted sea water temperature', 'units':'Kelvin', 'comments': 'Estimated one standard error of near-surface sea water temperature estimate from drifting buoy measurements'}),
                err_sst1=(['obs'], self.err_sst1, {'long_name': 'Standard uncertainty of fitted non-diurnal sea water temperature', 'units':'Kelvin', 'comments': 'Estimated one standard error of near-surface non-diurnal sea water temperature estimate from drifting buoy measurements'}),
                err_sst2=(['obs'], self.err_sst2, {'long_name': 'Standard uncertainty of fitted diurnal sea water temperature anomaly', 'units':'Kelvin', 'comments': 'Estimated one standard error of near-surface diurnal sea water temperature anomaly estimate from drifting buoy measurements'}),
                flg_sst=(['obs'], self.flg_sst, {'long_name': 'Fitted sea water temperature quality flag', 'units':'-', 'flag_values':'0, 1, 2, 3, 4, 5', 'flag_meanings': 'no-estimate, no-uncertainty-estimate, estimate-not-in-range-uncertainty-not-in-range, estimate-not-in-range-uncertainty-in-range estimate-in-range-uncertainty-not-in-range, estimate-in-range-uncertainty-in-range'}),
                flg_sst1=(['obs'], self.flg_sst1, {'long_name': 'Fitted non-diurnal sea water temperature quality flag', 'units':'-', 'flag_values':'0, 1, 2, 3, 4, 5', 'flag_meanings': 'no-estimate, no-uncertainty-estimate, estimate-not-in-range-uncertainty-not-in-range, estimate-not-in-range-uncertainty-in-range estimate-in-range-uncertainty-not-in-range, estimate-in-range-uncertainty-in-range'}),
                flg_sst2=(['obs'], self.flg_sst2, {'long_name': 'Fitted diurnal sea water temperature anomaly quality flag', 'units':'-', 'flag_values':'0, 1, 2, 3, 4, 5', 'flag_meanings': 'no-estimate, no-uncertainty-estimate, estimate-not-in-range-uncertainty-not-in-range, estimate-not-in-range-uncertainty-in-range estimate-in-range-uncertainty-not-in-range, estimate-in-range-uncertainty-in-range'}),
             ),

            coords=dict(
                ID=(['traj'], self.id, {'long_name': 'Global Drifter Program Buoy ID', 'units':'-'}),
                longitude=(['obs'], self.longitude, {'long_name': 'Longitude', 'units':'degrees_east'}),
                latitude=(['obs'], self.latitude, {'long_name': 'Latitude', 'units':'degrees_north'}),
                time=(['obs'], self.time, {'long_name': 'Time'}),
                ids=(['obs'], np.repeat(self.id, self.rowsize), {'long_name': "Trajectory index of vars['traj'] for all observations", 'units':'-'}),
            ),

            attrs={
                'title': 'Global Drifter Program hourly drifting buoy collection',
                'history': 'Version 2.00.  Metadata from dirall.dat and deplog.dat',
                'Conventions': 'CF-1.6',
                'date_created': datetime.now().isoformat(),
                'publisher_name': 'GDP Drifter DAC',
                'publisher_email': 'aoml.dftr@noaa.gov',
                'publisher_url': 'https://www.aoml.noaa.gov/phod/gdp',
                'licence': 'MIT License',
                'processing_level': 'Level 2 QC by GDP drifter DAC',
                'metadata_link': 'https://www.aoml.noaa.gov/phod/dac/dirall.html',
                'contributor_name': 'NOAA Global Drifter Program',
                'contributor_role': 'Data Acquisition Center',
                'institution': 'NOAA Atlantic Oceanographic and Meteorological Laboratory',
                'acknowledgement': 'Elipot et al. (2022) to be submitted. Elipot et al. (2016). Global Drifter Program quality-controlled hourly interpolated data from ocean surface drifting buoys, version 2.00. NOAA National Centers for Environmental Information. https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JC011716TBA. Accessed [date].',
                'summary': 'Global Drifter Program hourly data'
            }
        )

        ds.deploy_date.encoding['units'] = 'seconds since 1970-01-01 00:00:00'
        ds.end_date.encoding['units'] = 'seconds since 1970-01-01 00:00:00'
        ds.drogue_lost_date.encoding['units'] = 'seconds since 1970-01-01 00:00:00'
        ds.time.encoding['units'] = 'seconds since 1970-01-01 00:00:00'

        return ds


def create_ak(ds: xr.Dataset) -> ak.Array:
    # pointer to the start of each trajectory
    offset = ak.layout.Index32(np.insert(np.cumsum(ds.rowsize), 0, 0))
    longitude = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.longitude), parameters={'attrs': ds.longitude.attrs})
    latitude = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.latitude), parameters={'attrs': ds.latitude.attrs})
    time = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.time.values), parameters={'attrs': ds.time.attrs})
    ids = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.ids), parameters={'attrs': ds.ids.attrs})
    ve = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.ve), parameters={'attrs': ds.ve.attrs})
    vn = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.vn), parameters={'attrs': ds.vn.attrs})
    gap = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.gap), parameters={'attrs': ds.gap.attrs})
    err_lat = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_lat), parameters={'attrs': ds.err_lat.attrs})
    err_lon = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_lon), parameters={'attrs': ds.err_lon.attrs})
    err_ve = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_ve), parameters={'attrs': ds.err_ve.attrs})
    err_vn = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_vn), parameters={'attrs': ds.err_vn.attrs})
    drogue_status = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.drogue_status), parameters={'attrs': ds.drogue_status.attrs})
    sst = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.sst), parameters={'attrs': ds.sst.attrs})
    sst1 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.sst1), parameters={'attrs': ds.sst1.attrs})
    sst2 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.sst2), parameters={'attrs': ds.sst2.attrs})
    err_sst = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_sst), parameters={'attrs': ds.err_sst.attrs})
    err_sst1 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_sst1), parameters={'attrs': ds.err_sst1.attrs})
    err_sst2 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.err_sst2), parameters={'attrs': ds.err_sst2.attrs})
    flg_sst = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.flg_sst), parameters={'attrs': ds.flg_sst.attrs})
    flg_sst1 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.flg_sst1), parameters={'attrs': ds.flg_sst1.attrs})
    flg_sst2 = ak.layout.ListOffsetArray32(offset, ak.layout.NumpyArray(ds.flg_sst2), parameters={'attrs': ds.flg_sst2.attrs})

    obs = ak.Array(
        ak.layout.RecordArray(
            [
                longitude,
                latitude,
                time,
                ids,
                ve,
                vn,
                gap,
                err_lat,
                err_lon,
                err_ve,
                err_vn,
                drogue_status,
                sst,
                sst1,
                sst2,
                err_sst,
                err_sst1,
                err_sst2,
                flg_sst,
                flg_sst1,
                flg_sst2,
            ],
            [
                'longitude',
                'latitude',
                'time',
                'ids',
                've',
                'vn',
                'gap',
                'err_lat',
                'err_lon',
                'err_ve',
                'err_vn',
                'drogue_status',
                'sst',
                'sst1',
                'sst2',
                'err_sst',
                'err_sst1',
                'err_sst2',
                'flg_sst',
                'flg_sst1',
                'flg_sst2',
            ],
        )
    )
    
    # the string formats "S" and "U" are not supported as NumpyArray primitives
    # In that situation, we used `ak.with_parameters` that calls `ak.from_numpy` instead 
    # to convert from `S15` to variable length bytestrings. This is a temporary solution,
    # we are currently working on a dedicated parameters/attributes for Awkward Array
    array = ak.Array(
        ak.layout.RecordArray(
            [
                ak.layout.NumpyArray(ds.ID, parameters={'attrs': ds.ID.attrs}),
                ak.layout.NumpyArray(ds.rowsize, parameters={'attrs': ds.rowsize.attrs}),
                ak.layout.NumpyArray(ds.location_type, parameters={'attrs': ds.location_type.attrs}),
                ak.layout.NumpyArray(ds.WMO, parameters={'attrs': ds.WMO.attrs}),                
                ak.layout.NumpyArray(ds.expno, parameters={'attrs': ds.expno.attrs}),               
                ak.layout.NumpyArray(ds.deploy_date.values, parameters={'attrs': ds.deploy_date.attrs}),
                ak.layout.NumpyArray(ds.deploy_lat, parameters={'attrs': ds.deploy_lat.attrs}),
                ak.layout.NumpyArray(ds.deploy_lon, parameters={'attrs': ds.deploy_lon.attrs}),
                ak.layout.NumpyArray(ds.end_date.values, parameters={'attrs': ds.end_date.attrs}),
                ak.layout.NumpyArray(ds.end_lat, parameters={'attrs': ds.end_lat.attrs}),
                ak.layout.NumpyArray(ds.end_lon, parameters={'attrs': ds.end_lon.attrs}),
                ak.layout.NumpyArray(ds.drogue_lost_date.values, parameters={'attrs': ds.drogue_lost_date.attrs}),
                ak.layout.NumpyArray(ds.type_death, parameters={'attrs': ds.type_death.attrs}),
                ak.with_parameter(ds.type_buoy.values, 'attrs', ds.type_buoy.attrs, highlevel=False),
                ak.with_parameter(ds.DeploymentShip.values, 'attrs', ds.DeploymentShip.attrs, highlevel=False),
                ak.with_parameter(ds.DeploymentStatus.values, 'attrs', ds.DeploymentStatus.attrs, highlevel=False),
                ak.with_parameter(ds.BuoyTypeManufacturer.values, 'attrs',ds.BuoyTypeManufacturer.attrs, highlevel=False),
                ak.with_parameter(ds.BuoyTypeSensorArray.values, 'attrs', ds.BuoyTypeSensorArray.attrs, highlevel=False),
                ak.layout.NumpyArray(ds.CurrentProgram, parameters={'attrs': ds.CurrentProgram.attrs}),
                ak.with_parameter(ds.PurchaserFunding.values, 'attrs', ds.PurchaserFunding.attrs, highlevel=False),
                ak.with_parameter(ds.SensorUpgrade.values, 'attrs', ds.SensorUpgrade.attrs, highlevel=False),
                ak.with_parameter(ds.Transmissions.values, 'attrs', ds.Transmissions.attrs, highlevel=False),
                ak.with_parameter(ds.DeployingCountry.values, 'attrs', ds.DeployingCountry.attrs, highlevel=False),
                ak.with_parameter(ds.DeploymentComments.values, 'attrs', ds.DeploymentComments.attrs, highlevel=False),
                ak.layout.NumpyArray(ds.ManufactureYear, parameters={'attrs': ds.ManufactureYear.attrs}),
                ak.layout.NumpyArray(ds.ManufactureMonth, parameters={'attrs': ds.ManufactureMonth.attrs}),
                ak.with_parameter(ds.ManufactureSensorType.values, 'attrs', ds.ManufactureSensorType.attrs, highlevel=False),
                ak.layout.NumpyArray(ds.ManufactureVoltage, parameters={'attrs': ds.ManufactureVoltage.attrs}),
                ak.layout.NumpyArray(ds.FloatDiameter, parameters={'attrs': ds.FloatDiameter.attrs}),
                ak.layout.NumpyArray(ds.SubsfcFloatPresence, parameters={'attrs': ds.SubsfcFloatPresence.attrs}),
                ak.with_parameter(ds.DrogueType.values, 'attrs', ds.DrogueType.attrs, highlevel=False),
                ak.layout.NumpyArray(ds.DrogueLength, parameters={'attrs': ds.DrogueLength.attrs}),
                ak.layout.NumpyArray(ds.DrogueBallast, parameters={'attrs': ds.DrogueBallast.attrs}),
                ak.layout.NumpyArray(ds.DragAreaAboveDrogue, parameters={'attrs': ds.DragAreaAboveDrogue.attrs}),
                ak.layout.NumpyArray(ds.DragAreaOfDrogue, parameters={'attrs': ds.DragAreaOfDrogue.attrs}),
                ak.layout.NumpyArray(ds.DragAreaRatio, parameters={'attrs': ds.DragAreaRatio.attrs}),
                ak.layout.NumpyArray(ds.DrogueCenterDepth, parameters={'attrs': ds.DrogueCenterDepth.attrs}),
                ak.with_parameter(ds.DrogueDetectSensor.values, 'attrs', ds.DrogueDetectSensor.attrs, highlevel=False),
                obs.layout,
            ],
            [
                'ID',
                'rowsize',
                'location_type',
                'WMO',
                'expno',
                'deploy_date',
                'deploy_lat',
                'deploy_lon',
                'end_date',
                'end_lat',
                'end_lon',
                'drogue_lost_date',
                'type_death',
                'type_buoy',
                'DeploymentShip',
                'DeploymentStatus',
                'BuoyTypeManufacturer',
                'BuoyTypeSensorArray',
                'CurrentProgram',
                'PurchaserFunding',
                'SensorUpgrade',
                'Transmissions',
                'DeployingCountry',
                'DeploymentComments',
                'ManufactureYear',
                'ManufactureMonth',
                'ManufactureSensorType',
                'ManufactureVoltage',
                'FloatDiameter',
                'SubsfcFloatPresence',
                'DrogueType',
                'DrogueLength',
                'DrogueBallast',
                'DragAreaAboveDrogue',
                'DragAreaOfDrogue',
                'DragAreaRatio',
                'DrogueCenterDepth',
                'DrogueDetectSensor',
                'obs',
            ],
            parameters={'attrs': ds.attrs}  # global attributes
        )
    )
    return array
