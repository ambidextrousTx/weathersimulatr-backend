from herbie import Herbie
from pathlib import Path
import argparse


def load_wind_field(run_time):
    '''
    Returns an xrray dataset with
    u10, v10, wind_speed, wind_dir, lat, lon
    '''
    H = Herbie(run_time, model='hrrr', product='sfc', fxx=0)

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


def main():
    print("Hello from weathersimulatr-backend!")
    parser = argparse.ArgumentParser(
        description='Process weather data for visualization')
    parser.add_argument('timestamp', type=str,
                        help='the time stamp for which to get data')
    args = parser.parse_args()

    ds = load_wind_field(args.timestamp)
    print('-- Diagnostics --')
    print(ds)
    print('-- Diagnostics -- Dimensions')
    print(ds.dims)
    print('-- Diagnostics -- Coordinates')
    print(ds.coords)
    print('-- Diagnostics --')

    # Make an output directory
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    # Simple naming scheme
    out_path = out_dir / f"wind_{args.timestamp.replace(':', '').replace('-', '').replace('T', '_')}.nc"

    ds.to_netcdf(out_path)

    print(f"Saved wind field to {out_path}")


if __name__ == "__main__":
    main()
