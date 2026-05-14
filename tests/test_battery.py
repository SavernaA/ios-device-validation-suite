import pytest
from utils.device_simulator import IOSDeviceSimulator
from utils.thresholds import BATTERY

@pytest.fixture
def healthy_battery():
    return IOSDeviceSimulator(mode="healthy").get_battery()

@pytest.fixture
def degraded_battery():
    return IOSDeviceSimulator(mode="degraded").get_battery()

@pytest.fixture
def failing_battery():
    return IOSDeviceSimulator(mode="failing").get_battery()

class TestBatteryHealth:
    def test_capacity_meets_minimum(self, healthy_battery):
        assert healthy_battery.capacity_pct >= BATTERY["min_capacity_pct"]

    def test_capacity_not_above_100(self, healthy_battery):
        assert healthy_battery.capacity_pct <= 100.0

    def test_current_mah_consistent_with_health(self, healthy_battery):
        expected = healthy_battery.design_capacity_mah * (healthy_battery.capacity_pct / 100)
        tolerance = healthy_battery.design_capacity_mah * 0.05
        assert abs(healthy_battery.current_capacity_mah - expected) <= tolerance

class TestBatteryCycleCount:
    def test_cycle_count_within_range(self, healthy_battery):
        assert healthy_battery.cycle_count <= BATTERY["max_cycle_count"]

    def test_cycle_count_non_negative(self, healthy_battery):
        assert healthy_battery.cycle_count >= 0

    def test_failing_device_high_cycle_count(self, failing_battery):
        assert failing_battery.cycle_count > BATTERY["max_cycle_count"]

class TestBatteryVoltage:
    def test_voltage_within_safe_range(self, healthy_battery):
        assert BATTERY["min_voltage_mv"] <= healthy_battery.voltage_mv <= BATTERY["max_voltage_mv"]

    def test_failing_device_undervoltage(self, failing_battery):
        assert failing_battery.voltage_mv < BATTERY["min_voltage_mv"]

class TestBatteryTemperature:
    def test_temperature_within_range(self, healthy_battery):
        assert BATTERY["min_temp_celsius"] <= healthy_battery.temperature_celsius <= BATTERY["max_temp_celsius"]

    def test_failing_device_overtemperature(self, failing_battery):
        assert failing_battery.temperature_celsius > BATTERY["max_temp_celsius"]

class TestBatteryCharging:
    def test_charge_rate_positive_when_charging(self, healthy_battery):
        if healthy_battery.is_charging:
            assert healthy_battery.charge_rate_pct_per_min > 0

@pytest.mark.parametrize("capacity,expected_pass", [
    (100.0, True), (90.0, True), (80.0, True),
    (79.9, False), (50.0, False), (0.0, False),
])
def test_battery_capacity_boundary(capacity, expected_pass):
    assert (capacity >= BATTERY["min_capacity_pct"]) == expected_pass
