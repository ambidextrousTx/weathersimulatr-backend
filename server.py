from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import dataprocessing as dp
import xarray as xr

app = FastAPI()

DATA_PATH = Path("data/wind_20170826_0300.nc")


# Helpers #
def load_netcdf():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")
    return xr.open_dataset(DATA_PATH)


# API #
@app.get("/wind/harvey")
def get_wind_harvey():
    try:
        data = load_netcdf()
        harvey_wind_payload = dp.wind_payload_from_dataset(data)
        return JSONResponse(content=harvey_wind_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return "ok"
