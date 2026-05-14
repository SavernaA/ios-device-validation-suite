import random
from dataclasses import dataclass

@dataclass
class BatteryData:
    capacity_pct: float
    cycle_count: int
    voltage_mv: float
    temperature_celsius: float
    is_charging: bool
    charge_rate_pct_per_min: float
    design_capacity_mah: int
    current_capacity_mah: int

@dataclass
class StorageData:
    total_gb: float
    used_gb: float
    free_gb: float
    read_speed_mbps: float
    write_speed_mbps: float
    read_latency_ms: float
    write_latency_ms: float
    bad_block_count: int
    filesystem: str = "APFS"

@dataclass
class CPUData:
    core_count: int
    idle_usage_pct: float
    temperature_celsius: float
    benchmark_score: int
    boot_time_seconds: float
    app_launch_seconds: float
    sustained_perf_drop_pct: float
    chip_model: str = "Apple A17 Pro"

@dataclass
class SensorData:
    accel_noise_mg: float
    accel_range_g: float
    gyro_drift_dps: float
    gyro_range_dps: float
    proximity_response_ms: float
    proximity_detected: bool
    ambient_light_lux: float
    gps_accuracy_meters: float
    gps_ttff_seconds: float
    gps_satellites: int
    barometric_pressure_hpa: float
    baro_accuracy_hpa: float
    touch_latency_ms: float
    touch_sample_rate_hz: float

class IOSDeviceSimulator:
    def __init__(self, mode="healthy", device_model="iPhone 15 Pro"):
        assert mode in ("healthy", "degraded", "failing")
        self.mode = mode
        self.device_model = device_model

    def get_battery(self):
        if self.mode == "healthy":
            cap, cyc = random.uniform(88, 100), random.randint(10, 250)
            volt, temp = random.uniform(3800, 4200), random.uniform(22, 38)
        elif self.mode == "degraded":
            cap, cyc = random.uniform(78, 87), random.randint(400, 520)
            volt, temp = random.uniform(3650, 3800), random.uniform(40, 48)
        else:
            cap, cyc = random.uniform(50, 75), random.randint(600, 900)
            volt, temp = random.uniform(3200, 3599), random.uniform(50, 65)
        return BatteryData(
            capacity_pct=cap, cycle_count=cyc, voltage_mv=volt,
            temperature_celsius=temp, is_charging=random.choice([True, False]),
            charge_rate_pct_per_min=random.uniform(0.8, 1.5),
            design_capacity_mah=3274, current_capacity_mah=int(3274 * cap / 100),
        )

    def get_storage(self):
        if self.mode == "healthy":
            total = random.choice([128.0, 256.0, 512.0, 1024.0])
            used = random.uniform(10, total * 0.6)
            rs, ws = random.uniform(1800, 2500), random.uniform(1000, 1800)
            rl, wl = random.uniform(5, 25), random.uniform(30, 60)
            bad = 0
        elif self.mode == "degraded":
            total, used = 128.0, random.uniform(120, 126)
            rs, ws = random.uniform(600, 900), random.uniform(150, 220)
            rl, wl = random.uniform(45, 70), random.uniform(90, 130)
            bad = 0
        else:
            total, used = 128.0, random.uniform(127.1, 127.9)
            rs, ws = random.uniform(100, 400), random.uniform(50, 150)
            rl, wl = random.uniform(100, 300), random.uniform(200, 500)
            bad = random.randint(1, 5)
        return StorageData(
            total_gb=total, used_gb=used, free_gb=total-used,
            read_speed_mbps=rs, write_speed_mbps=ws,
            read_latency_ms=rl, write_latency_ms=wl, bad_block_count=bad,
        )

    def get_cpu(self):
        if self.mode == "healthy":
            return CPUData(core_count=6, idle_usage_pct=random.uniform(0.5, 4.0),
                temperature_celsius=random.uniform(28, 45),
                benchmark_score=random.randint(2000, 2800),
                boot_time_seconds=random.uniform(18, 35),
                app_launch_seconds=random.uniform(0.8, 2.0),
                sustained_perf_drop_pct=random.uniform(5, 15))
        elif self.mode == "degraded":
            return CPUData(core_count=6, idle_usage_pct=random.uniform(6, 15),
                temperature_celsius=random.uniform(55, 65),
                benchmark_score=random.randint(1200, 1600),
                boot_time_seconds=random.uniform(40, 55),
                app_launch_seconds=random.uniform(3.5, 6.0),
                sustained_perf_drop_pct=random.uniform(18, 25))
        else:
            return CPUData(core_count=4, idle_usage_pct=random.uniform(20, 60),
                temperature_celsius=random.uniform(65, 80),
                benchmark_score=random.randint(500, 1100),
                boot_time_seconds=random.uniform(60, 120),
                app_launch_seconds=random.uniform(8, 20),
                sustained_perf_drop_pct=random.uniform(30, 60))

    def get_sensors(self):
        if self.mode == "healthy":
            return SensorData(
                accel_noise_mg=random.uniform(1, 7), accel_range_g=8,
                gyro_drift_dps=random.uniform(0.001, 0.03), gyro_range_dps=250,
                proximity_response_ms=random.uniform(10, 35), proximity_detected=True,
                ambient_light_lux=random.uniform(100, 10000),
                gps_accuracy_meters=random.uniform(2, 8),
                gps_ttff_seconds=random.uniform(15, 45),
                gps_satellites=random.randint(8, 15),
                barometric_pressure_hpa=random.uniform(1005, 1025),
                baro_accuracy_hpa=random.uniform(0.1, 0.8),
                touch_latency_ms=random.uniform(8, 22), touch_sample_rate_hz=120)
        elif self.mode == "degraded":
            return SensorData(
                accel_noise_mg=random.uniform(8, 14), accel_range_g=8,
                gyro_drift_dps=random.uniform(0.04, 0.08), gyro_range_dps=250,
                proximity_response_ms=random.uniform(45, 80), proximity_detected=True,
                ambient_light_lux=random.uniform(0, 500),
                gps_accuracy_meters=random.uniform(9, 18),
                gps_ttff_seconds=random.uniform(50, 75),
                gps_satellites=random.randint(3, 6),
                barometric_pressure_hpa=random.uniform(1000, 1030),
                baro_accuracy_hpa=random.uniform(0.9, 1.5),
                touch_latency_ms=random.uniform(28, 45), touch_sample_rate_hz=60)
        else:
            return SensorData(
                accel_noise_mg=random.uniform(15, 30), accel_range_g=4,
                gyro_drift_dps=random.uniform(0.1, 0.5), gyro_range_dps=125,
                proximity_response_ms=random.uniform(100, 300), proximity_detected=False,
                ambient_light_lux=random.uniform(0, 50),
                gps_accuracy_meters=random.uniform(20, 100),
                gps_ttff_seconds=random.uniform(80, 180),
                gps_satellites=random.randint(0, 2),
                barometric_pressure_hpa=random.uniform(990, 1040),
                baro_accuracy_hpa=random.uniform(2.0, 5.0),
                touch_latency_ms=random.uniform(60, 200), touch_sample_rate_hz=30)
