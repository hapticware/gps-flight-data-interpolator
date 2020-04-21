import pytest

from flight_data import __version__
from flight_data.monitor import Monitor
from flight_data.location_stream import LocationStream


def test_version():
    assert __version__ == "0.0.1"


@pytest.fixture
def climbing_left_turn_log():
    """
    Emulate a coordinate/location sample rate of 2 per second, turning
    left at 120 KTS and climbing at 300 FPM.

    What we really want here is a standard rate turn but I'm using approximated
    coordinates and it turned out to be a bit less than standard rate. We'll
    revisit this later and clean up the fixture data using a proper formula to
    derive the correct coordinates based on the speed.
    """

    return LocationStream(
        [
            [39.989382, -100.000000, 1000.0, 1587702253000],
            [39.989389, -100.000363, 1002.5, 1587702252500],
            [39.989396, -100.000725, 1005.0, 1587702252000],
            [39.989418, -100.001087, 1007.5, 1587702251500],
            [39.989440, -100.001449, 1010.0, 1587702251000],
            [39.989477, -100.001808, 1012.5, 1587702250500],
            [39.989513, -100.002168, 1015.0, 1587702250000],
            [39.989564, -100.002524, 1017.5, 1587702249500],
            [39.989615, -100.002881, 1020.0, 1587702249000],
            [39.989681, -100.003234, 1022.5, 1587702248500],
            [39.989746, -100.003586, 1025.0, 1587702248000],
            [39.989825, -100.003934, 1027.5, 1587702247500],
            [39.989905, -100.004281, 1030.0, 1587702247000],
            [39.989998, -100.004623, 1032.5, 1587702246500],
            [39.990092, -100.004964, 1035.0, 1587702246000],
            [39.990199, -100.005299, 1037.5, 1587702245500],
            [39.990306, -100.005633, 1040.0, 1587702245000],
            [39.990426, -100.005960, 1042.5, 1587702244500],
            [39.990546, -100.006287, 1045.0, 1587702244000],
            [39.990680, -100.006605, 1047.5, 1587702243500],
            [39.990813, -100.006923, 1050.0, 1587702243000],
            [39.990959, -100.007231, 1052.5, 1587441160500],
        ]
    )


@pytest.fixture
def straight_and_level_log():
    """
    We'll test that straight and level flight returns proper metrics from the
    monitor, but also add some spurious high-frequency samples that should be
    discarded and would otherwise cause non-zero turn and climb rates.
    """
    return LocationStream(
        [
            [40.000000, -100.000000, 1000.0, 1587702253000],
            [39.989382, -100.000000, 1200.0, 1587702252900],  # Spurious
            [39.988382, -100.000000, 1400.0, 1587702252800],  # Spurious
            [40.000000, -100.000000, 1000.0, 1587702252500],
            [40.000000, -100.000000, 1000.0, 1587702252000],
            [40.000000, -100.000000, 1000.0, 1587702251000],
            [40.000000, -100.000000, 1000.0, 1587702250000],
        ]
    )


# NOTE: This tests the basic turn rate calculations but it also implicitly
# confirms the lookback timeframe because this full log demonstrates a turn
# that is shallowing (the full average is something like -3.2 degrees/second).
# The fact that we see a lower number indicates that we are in fact restricting
# ourselves to a shorter timeframe.
def test_monitor_turn_rate(climbing_left_turn_log, straight_and_level_log):
    assert Monitor(climbing_left_turn_log).turn_rate() == -2.4
    assert Monitor(straight_and_level_log).turn_rate() == 0
