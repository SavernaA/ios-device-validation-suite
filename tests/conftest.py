import pytest
from utils.device_simulator import IOSDeviceSimulator

def pytest_configure(config):
    config.addinivalue_line("markers", "hardware: hardware validation tests")
    config.addinivalue_line("markers", "performance: performance tests")
    config.addinivalue_line("markers", "sensor: sensor tests")
    config.addinivalue_line("markers", "negative: negative test cases")
    config.addinivalue_line("markers", "boundary: boundary value analysis tests")

@pytest.fixture(scope="session")
def healthy_device():
    return IOSDeviceSimulator(mode="healthy", device_model="iPhone 15 Pro")

@pytest.fixture(scope="session")
def degraded_device():
    return IOSDeviceSimulator(mode="degraded", device_model="iPhone 13")

@pytest.fixture(scope="session")
def failing_device():
    return IOSDeviceSimulator(mode="failing", device_model="iPhone 11")
