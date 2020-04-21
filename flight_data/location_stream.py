from flight_data.location_sample import LocationSample


class LocationStream:
    def __init__(self, raw_samples):
        self.samples = self.__convert_raw_samples(raw_samples)

    def __convert_raw_samples(self, raw_samples):
        return map(lambda sample: LocationSample(*sample), raw_samples)
