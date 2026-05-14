import pytest
from utils.device_simulator import IOSDeviceSimulator
from utils.thresholds import SENSORS

@pytest.fixture
def healthy_sensors():
    return IOSDeviceSimulator(mode="healthy").get_sensors()

@pytest.fixture
def failing_sensors():
    return IOSDeviceSimulator(mode="failing").get_sensors()

class TestAccelerometer:
    def test_noise_within_limit(self, healthy_sensors):
        assert healthy_sensors.accel_noise_mg <= SENSORS["accel_max_noise_mg"]

    def test_range_sufficient(self, healthy_sensors):
        assert healthy_sensors.accel_range_g >= SENSORS["accel_range_g"]

    def test_failing_excessive_noise(self, failing_sensors):
        assert failing_sensors.accel_noise_mg > SENSORS["accel_max_noise_mg"]

class TestGyroscope:
    def test_drift_within_spec(self, healthy_sensors):
        assert healthy_sensors.gyro_drift_dps <= SENSORS["gyro_max_drift_dps"]

    def test_range_sufficient(self, healthy_sensors):
        assert healthy_sensors.gyro_range_dps >= SENSORS["gyro_range_dps"]

    def test_failing_excessive_drift(self, failing_sensors):
        assert failing_sensors.gyro_drift_dps > SENSORS["gyro_max_drift_dps"]

class TestGPS:
    def test_accuracy_within_spec(self, healthy_sensors):
        assert healthy_sensors.gps_accuracy_meters <= SENSORS["gps_accuracy_meters"]

    def test_ttff_within_spec(self, healthy_sensors):
        assert healthy_sensors.gps_ttff_seconds <= SENSORS["gps_ttff_seconds"]

    def test_minimum_satellite_count(self, healthy_sensors):
        assert healthy_sensors.gps_satellites >= 4

    def test_failing_poor_gps(self, failing_sensors):
        assert failing_sensors.gps_accuracy_meters > SENSORS["gps_accuracy_meters"] or \
               failing_sensors.gps_satellites < 4

class TestProximitySensor:
    def test_response_within_spec(self, healthy_sensors):
        assert healthy_sensors.proximity_response_ms <= SENSORS["proximity_response_ms"]

    def test_detects_object(self, healthy_sensors):
        assert healthy_sensors.proximity_detected is True

    def test_failing_unresponsive(self, failing_sensors):
        assert failing_sensors.proximity_detected is False

class TestAmbientLight:
    def test_reading_in_valid_range(self, healthy_sensors):
        assert SENSORS["als_min_lux"] <= healthy_sensors.ambient_light_lux <= SENSORS["als_max_lux"]

class TestBarometer:
    def test_accuracy_within_spec(self, healthy_sensors):
        assert healthy_sensors.baro_accuracy_hpa <= SENSORS["baro_accuracy_hpa"]

    def test_pressure_in_realistic_range(self, healthy_sensors):
        assert 870 <= healthy_sensors.barometric_pressure_hpa <= 1084

class TestTouchscreen:
    def test_latency_within_spec(self, healthy_sensors):
        assert healthy_sensors.touch_latency_ms <= SENSORS["touch_latency_ms"]

    def test_sample_rate_meets_minimum(self, healthy_sensors):
        assert healthy_sensors.touch_sample_rate_hz >= SENSORS["touch_sample_rate_hz"]

    def test_failing_poor_touch(self, failing_sensors):
        assert failing_sensors.touch_latency_ms > SENSORS["touch_latency_ms"] or \
               failing_sensors.touch_sample_rate_hz < SENSORS["touch_sample_rate_hz"]

@pytest.mark.parametrize("accuracy_m,expected_pass", [
    (1.0, True), (5.0, True), (10.0, True),
    (10.1, False), (50.0, False), (100, False),
])
def test_gps_accuracy_boundary(accuracy_m, expected_pass):
    assert (accuracy_m <= SENSORS["gps_accuracy_meters"]) == expected_pass
