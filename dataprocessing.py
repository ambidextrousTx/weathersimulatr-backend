from herbie import Herbie

TEXAS_LAT_MIN = 25.0
TEXAS_LAT_MAX = 36.5
TEXAS_LON_MIN = 253.4
TEXAS_LON_MAX = 266.5  # -106.6 to -93.5


def crop_harvey_texas(ds, step=5):
    """
    Crop the full HRRR CONUS field to a Texas/Harvey bounding box,
    and subsample every `step` grid points in y and x.
    """

    lat = ds["latitude"]
    lon = ds["longitude"]

    # Texas-like bounding box in the 0–360 longitude domain
    lat_min, lat_max = TEXAS_LAT_MIN, TEXAS_LAT_MAX
    lon_min, lon_max = TEXAS_LON_MIN, TEXAS_LON_MAX

    mask = (
        (lat >= lat_min)
        & (lat <= lat_max)
        & (lon >= lon_min)
        & (lon <= lon_max)
    )

    # Mask all variables, then drop points outside box
    ds_box = ds.where(mask, drop=True)

    # Subsample to make the grid lighter for the frontend
    ds_sub = ds_box.isel(y=slice(0, None, step), x=slice(0, None, step))

    return ds_sub


def wind_payload_from_dataset(ds):
    """
    Turn cropped ds into a JSON-serializable payload.
    Note: as-list conversion is only for debugging / first pass;
    we’ll optimize later.
    """

    wind = extract_wind_field(ds)
    lat = wind["lat"].values
    lon = wind["lon"].values
    speed = wind["speed"].values
    direction = wind["direction"].values

    return {
        "time": str(ds["valid_time"].values.item()),
        "shape": {
            "y": lat.shape[0],
            "x": lat.shape[1],
        },
        "lat": lat.tolist(),
        "lon": lon.tolist(),
        "speed": speed.tolist(),
        "direction": direction.tolist(),
    }


def extract_wind_field(ds):
    """
    Given the xarray.Dataset from load_wind_field_for_timestamp, return a dict with:
      - lat, lon: 2D arrays
      - speed: 2D array (si10)
      - direction: 2D array (wdir10)
    """

    lat = ds["latitude"]
    lon = ds["longitude"]
    speed = ds["si10"]
    direction = ds["wdir10"]

    return {
        "lat": lat,
        "lon": lon,
        "speed": speed,
        "direction": direction,
    }


def load_wind_field_for_timestamp(timestamp_of_interest):
    '''
    Returns an xarray dataset with
    u10, v10, wind_speed, wind_dir, lat, lon
    '''
    H = Herbie(timestamp_of_interest, model='hrrr', product='sfc', fxx=0)

    # Look at the GRIB2 file contents
    # H.inventory()

    # Read a subset of the file with xarray, like 2-m temperature.
    dataset = H.xarray("GRD:10 m above").herbie.with_wind()

    # Narrow down to just what we care about for the frontend
    var_names = [v for v in dataset.data_vars if any(k in v.lower() for k in
                                                     ["10u", "10v", "si10",
                                                      "wdir10", "ws", "wdir"])]

    ds_out = dataset[var_names]

    # It’s okay if ds_out has extra metadata; we can refine later
    return ds_out
