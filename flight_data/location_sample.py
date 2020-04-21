from datetime import datetime


class LocationSample:
    def __init__(self, latitude, longitude, elevation, time):
        """
        Parameters:
        elevation (float): Units should be feet.
        time (int): Milliseconds since epoch
        """

        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.time = datetime.fromtimestamp(time / 1000)
