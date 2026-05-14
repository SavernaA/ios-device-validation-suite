BATTERY = {
    "min_capacity_pct": 80,
    "max_cycle_count": 500,
    "min_voltage_mv": 3600,
    "max_voltage_mv": 4350,
    "max_temp_celsius": 45.0,
    "min_temp_celsius": 0.0,
    "max_charge_time_minutes": 120,
    "charging_threshold_pct": 1,
}
STORAGE = {
    "min_free_space_gb": 1.0,
    "max_read_latency_ms": 50,
    "max_write_latency_ms": 100,
    "min_read_speed_mbps": 800,
    "min_write_speed_mbps": 200,
    "max_bad_block_count": 0,
    "min_total_storage_gb": 60,
}
CPU = {
    "max_idle_usage_pct": 5,
    "max_sustained_temp_celsius": 60.0,
    "min_benchmark_score": 1500,
    "max_boot_time_seconds": 45,
    "max_app_launch_seconds": 3.0,
    "min_cores": 6,
    "max_throttle_drop_pct": 20,
}
SENSORS = {
    "accel_max_noise_mg": 10,
    "accel_range_g": 8,
    "gyro_max_drift_dps": 0.05,
    "gyro_range_dps": 250,
    "proximity_response_ms": 50,
    "als_min_lux": 0,
    "als_max_lux": 40000,
    "gps_accuracy_meters": 10,
    "gps_ttff_seconds": 60,
    "baro_accuracy_hpa": 1.0,
    "touch_latency_ms": 30,
    "touch_sample_rate_hz": 120,
}
