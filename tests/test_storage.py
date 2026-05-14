import pytest
from utils.device_simulator import IOSDeviceSimulator
from utils.thresholds import STORAGE

@pytest.fixture
def healthy_storage():
    return IOSDeviceSimulator(mode="healthy").get_storage()

@pytest.fixture
def degraded_storage():
    return IOSDeviceSimulator(mode="degraded").get_storage()

@pytest.fixture
def failing_storage():
    return IOSDeviceSimulator(mode="failing").get_storage()

class TestStorageCapacity:
    def test_minimum_free_space(self, healthy_storage):
        assert healthy_storage.free_gb >= STORAGE["min_free_space_gb"]

    def test_total_meets_minimum(self, healthy_storage):
        assert healthy_storage.total_gb >= STORAGE["min_total_storage_gb"]

    def test_used_plus_free_equals_total(self, healthy_storage):
        assert abs((healthy_storage.used_gb + healthy_storage.free_gb) - healthy_storage.total_gb) < 0.01

    def test_failing_insufficient_free_space(self, failing_storage):
        assert failing_storage.free_gb < STORAGE["min_free_space_gb"]

    def test_filesystem_is_apfs(self, healthy_storage):
        assert healthy_storage.filesystem == "APFS"

class TestStorageSpeed:
    def test_read_speed_meets_minimum(self, healthy_storage):
        assert healthy_storage.read_speed_mbps >= STORAGE["min_read_speed_mbps"]

    def test_write_speed_meets_minimum(self, healthy_storage):
        assert healthy_storage.write_speed_mbps >= STORAGE["min_write_speed_mbps"]

    def test_read_faster_than_write(self, healthy_storage):
        assert healthy_storage.read_speed_mbps > healthy_storage.write_speed_mbps

    def test_degraded_slow_read(self, degraded_storage):
        assert degraded_storage.read_speed_mbps < STORAGE["min_read_speed_mbps"]

class TestStorageLatency:
    def test_read_latency_within_threshold(self, healthy_storage):
        assert healthy_storage.read_latency_ms <= STORAGE["max_read_latency_ms"]

    def test_write_latency_within_threshold(self, healthy_storage):
        assert healthy_storage.write_latency_ms <= STORAGE["max_write_latency_ms"]

    def test_read_latency_lower_than_write(self, healthy_storage):
        assert healthy_storage.read_latency_ms < healthy_storage.write_latency_ms

class TestStorageBadBlocks:
    def test_no_bad_blocks_healthy(self, healthy_storage):
        assert healthy_storage.bad_block_count == 0

    def test_bad_blocks_on_failing(self, failing_storage):
        assert failing_storage.bad_block_count > 0

@pytest.mark.parametrize("read_mbps,write_mbps,expected_pass", [
    (2000, 1500, True), (800, 200, True),
    (799, 200, False), (800, 199, False), (100, 50, False),
])
def test_storage_speed_boundary(read_mbps, write_mbps, expected_pass):
    passes = (read_mbps >= STORAGE["min_read_speed_mbps"]) and (write_mbps >= STORAGE["min_write_speed_mbps"])
    assert passes == expected_pass
