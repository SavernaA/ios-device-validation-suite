import pytest
from utils.device_simulator import IOSDeviceSimulator
from utils.thresholds import CPU

@pytest.fixture
def healthy_cpu():
    return IOSDeviceSimulator(mode="healthy").get_cpu()

@pytest.fixture
def failing_cpu():
    return IOSDeviceSimulator(mode="failing").get_cpu()

class TestCPUCoreCount:
    def test_minimum_core_count(self, healthy_cpu):
        assert healthy_cpu.core_count >= CPU["min_cores"]

    def test_failing_device_low_cores(self, failing_cpu):
        assert failing_cpu.core_count < CPU["min_cores"]

class TestCPUIdle:
    def test_idle_usage_within_threshold(self, healthy_cpu):
        assert healthy_cpu.idle_usage_pct <= CPU["max_idle_usage_pct"]

    def test_idle_usage_non_negative(self, healthy_cpu):
        assert healthy_cpu.idle_usage_pct >= 0

    def test_failing_device_high_idle(self, failing_cpu):
        assert failing_cpu.idle_usage_pct > CPU["max_idle_usage_pct"]

class TestCPUThermal:
    def test_temperature_within_limit(self, healthy_cpu):
        assert healthy_cpu.temperature_celsius <= CPU["max_sustained_temp_celsius"]

    def test_throttle_drop_within_limit(self, healthy_cpu):
        assert healthy_cpu.sustained_perf_drop_pct <= CPU["max_throttle_drop_pct"]

    def test_failing_device_thermal_overrun(self, failing_cpu):
        assert failing_cpu.temperature_celsius > CPU["max_sustained_temp_celsius"]

class TestCPUBenchmark:
    def test_benchmark_meets_minimum(self, healthy_cpu):
        assert healthy_cpu.benchmark_score >= CPU["min_benchmark_score"]

    def test_benchmark_is_positive(self, healthy_cpu):
        assert healthy_cpu.benchmark_score > 0

    def test_failing_device_low_benchmark(self, failing_cpu):
        assert failing_cpu.benchmark_score < CPU["min_benchmark_score"]

class TestCPULatency:
    def test_boot_time_within_threshold(self, healthy_cpu):
        assert healthy_cpu.boot_time_seconds <= CPU["max_boot_time_seconds"]

    def test_app_launch_within_threshold(self, healthy_cpu):
        assert healthy_cpu.app_launch_seconds <= CPU["max_app_launch_seconds"]

    def test_failing_device_slow_boot(self, failing_cpu):
        assert failing_cpu.boot_time_seconds > CPU["max_boot_time_seconds"]

    def test_failing_device_slow_launch(self, failing_cpu):
        assert failing_cpu.app_launch_seconds > CPU["max_app_launch_seconds"]

@pytest.mark.parametrize("score,expected_pass", [
    (2800, True), (1500, True), (1499, False), (1000, False), (0, False),
])
def test_benchmark_boundary(score, expected_pass):
    assert (score >= CPU["min_benchmark_score"]) == expected_pass
