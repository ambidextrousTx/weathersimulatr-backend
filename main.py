from herbie import Herbie


def main():
    print("Hello from weathersimulatr-backend!")

    # Create Herbie object for the HRRR model 6-hr surface forecast product
    H = Herbie(
            '2021-01-01 12:00',
            model='hrrr',
            product='sfc',
            fxx=6
            )

    # Look at the GRIB2 file contents
    H.inventory()

    # Download the full GRIB2 file
    # H.download()

    # Download a subset of the GRIB2 file, like all fields at 500 mb
    H.download(":500 mb")

    # Read a subset of the file with xarray, like 2-m temperature.
    H.xarray("TMP:2 m")


if __name__ == "__main__":
    main()
