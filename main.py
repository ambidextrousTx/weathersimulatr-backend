from pathlib import Path
import argparse
import dataprocessing as dp


HARVEY_TX_LANDFALL_TIME = "2017-08-26T03:00"


def main():
    print("Hello from weathersimulatr-backend!")
    parser = argparse.ArgumentParser(
        description='Process weather data for visualization')
    parser.add_argument('-t',
                        '--timestamp',
                        default=HARVEY_TX_LANDFALL_TIME,
                        type=str,
                        help='the time stamp for which to get data')
    args = parser.parse_args()

    wind_field_dataset = dp.load_wind_field_for_timestamp(args.timestamp)
    harvey_wind_dataset = dp.crop_harvey_texas(wind_field_dataset, step=5)
    # print_diagnostics(harvey_wind_dataset)

    # Extract wind payload
    harvey_wind_payload = dp.wind_payload_from_dataset(harvey_wind_dataset)
    print(f'Payload shape: {harvey_wind_payload["shape"]}')
    print(f'Min speed: {min(harvey_wind_payload["speed"])}')
    print(f'Max speed: {max(harvey_wind_payload["speed"])}')

    # Make an output directory
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    # Simple naming scheme
    out_path = out_dir / f"wind_{args.timestamp.replace(':', '').replace('-', '').replace('T', '_')}.nc"

    harvey_wind_dataset.to_netcdf(out_path)

    print(f"Saved cropped wind field to {out_path}")


if __name__ == "__main__":
    main()
