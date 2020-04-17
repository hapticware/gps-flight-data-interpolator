# GPS Flight Data Interpolator
A library to calculate and expose estimated flight data based on a GPS source, currently supporting raw GPS data and XPlane data via UDP. Only GPS latitude, longitude and elevation are assumed to be available so course, turn rate, vertical speed and other flight metrics are derived values and should be considered approximations.

## Setup

See `.tool-versions` for system dependencies, install
[Poetry](https://python-poetry.org/) and run `poetry install`.
