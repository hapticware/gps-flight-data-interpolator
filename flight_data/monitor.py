from datetime import timedelta
from statistics import mean
from math import atan2, cos, degrees, sin


class Monitor:
    # NOTE: For now we'll set a constant time to look back into the location
    # stream. This is one way to set senstivity—we want a large enough time
    # frame to get enough datapoints for an average to be established and
    # statistically significant, but if we set the time frame too large we may
    # miss minor changes (or not detect them fast enough to be helpful as a
    # near-real-time monitor). Eventually this should probably be configurable
    # since faster planes should have shorter timeframes.
    LOOKBACK_TIME = 2.0  # Seconds

    # NOTE: GPS systems can sample locations at very high rates. At typical
    # light aircraft speeds the distance between locations between two
    # high-frequency location samples will often be below the precision
    # capabilities of the GPS system. Since we only care about the delta between
    # location samples we need to ensure enough distance has elapsed that we can
    # be confident the change is due to movement as opposed to reading
    # variance/noise.
    MINIMUM_SAMPLE_INTERVAL = 500  # Milliseconds

    # Location streams act as arrays ordered by sample time where the first
    # value is the most recent sample and each entry provides latitude,
    # longitude and elevation.
    def __init__(self, location_stream):
        self.location_stream = location_stream

    def turn_rate(self):
        location_samples = self.__downsample_locations_in_lookback_frame()
        # NOTE: You need at least three points to calculate a turn rate:
        if len(location_samples) < 3:
            return None

        turn_rates = map(
            lambda i: self.__course_deviation_rate(location_samples[i : i + 3]),
            range(len(location_samples) - 2),
        )
        return mean(turn_rates)

    def __downsample_locations_in_lookback_frame(self):
        downsampled_locations = []
        latest_stream_time = None
        preceding_sample_time = None

        for location_sample in self.location_stream.samples:
            if (
                preceding_sample_time
                and preceding_sample_time
                - timedelta(milliseconds=self.MINIMUM_SAMPLE_INTERVAL)
                < location_sample.time
            ):
                continue
            if latest_stream_time and (
                location_sample.time
                < latest_stream_time - timedelta(seconds=self.LOOKBACK_TIME)
            ):
                return downsampled_locations

            downsampled_locations.append(location_sample)
            preceding_sample_time = location_sample.time
            latest_stream_time = latest_stream_time or location_sample.time

        return downsampled_locations

    def __course_deviation_rate(self, location_samples):
        """
        Return the rate of course change based on three timestamped coordinates.
        This is returned in degrees per second.
        """

        first_course = self.__true_course(*location_samples[0:2])
        second_course = self.__true_course(*location_samples[1:3])
        total_time = location_samples[0].time - location_samples[1].time
        return round((second_course - first_course) / total_time.total_seconds(), 1)

    def __true_course(self, location1, location2):
        """
        Calculate the bearing between two location samples based on their
        latitude and longitude values.
        """

        bearing = atan2(
            sin(location2.longitude - location1.longitude) * cos(location2.latitude),
            cos(location1.latitude) * sin(location2.latitude)
            - sin(location1.latitude)
            * cos(location2.latitude)
            * cos(location2.longitude - location1.longitude),
        )

        return degrees(bearing) % 360
