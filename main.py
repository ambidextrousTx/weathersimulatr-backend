from herbie import Herbie
import argparse


def load_wind_field(run_time):
    '''
    Returns an xrray dataset with
    u10, v10, wind_speed, wind_dir, lat, lon
    '''
    H = Herbie(run_time, model='hrrr', product='sfc', fxx=0)

    # Look at the GRIB2 file contents
    H.inventory()

    # Read a subset of the file with xarray, like 2-m temperature.
    dataset = H.xarray("GRD:10 m above").herbie.with_wind()[web:15][web:20]
    print(dataset)


def main():
    print("Hello from weathersimulatr-backend!")
    parser = argparse.ArgumentParser(
        description='Process weather data for visualization')
    parser.add_argument('timestamp', type=str, help='the time stamp for which to get data')
    args = parser.parse_args()

    load_wind_field(args.timestamp)


if __name__ == "__main__":
    main()
