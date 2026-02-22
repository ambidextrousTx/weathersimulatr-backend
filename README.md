# weathersimulatr-backend
A Python backend to process numeric weather prediction (NWP) data for 
visualization

Fetches and processes NWP data, processing real model fields (winds, pressure, 
precipitation) for specific storm events. The goal is to feed the processed 
data to a renderer which can be a separate service.

In particular, fetches and processes NWP data for Hurricane Harvey that hit the 
Texas coast on 2017-08-26T03:00

The data is stored locally under the folder data/, which has been .gitignored
