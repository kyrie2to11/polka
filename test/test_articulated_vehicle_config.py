from pathlib import Path

import yaml


CONFIG = Path(__file__).parents[1] / "config" / "articulated_vehicle.yaml"


def test_articulated_vehicle_uses_per_source_airy_imus():
    params = yaml.safe_load(CONFIG.read_text())["polka"]["ros__parameters"]
    assert params["motion_compensation"]["enabled"] is True
    assert params["motion_compensation"]["per_point_deskew"] is True
    assert params["source_names"] == ["airy_front", "airy_rear", "airy_left_front"]
    assert params["sources"]["airy_front"]["imu_topic"] == "/imu/airy_front"
    assert params["sources"]["airy_rear"]["imu_topic"] == "/imu/airy_rear"
    assert params["sources"]["airy_left_front"]["topic"] == "/pointcloud/airy_left_front"
    assert params["sources"]["airy_left_front"]["imu_topic"] == "/imu/airy_left_front"


def test_articulated_vehicle_preserves_full_lidar_range_at_five_cm():
    params = yaml.safe_load(CONFIG.read_text())["polka"]["ros__parameters"]
    for source in params["sources"].values():
        assert source["filters"]["range"] == {
            "enabled": True,
            "min": 0.2,
            "max": 200.0,
        }
    assert params["outputs"]["cloud"]["filters"]["range"] == {
        "enabled": True,
        "min": 0.2,
        "max": 200.0,
    }
    assert params["outputs"]["cloud"]["voxel"]["leaf_size"] == 0.05
    assert params["outputs"]["scan"]["range_min"] == 0.2
    assert params["outputs"]["scan"]["range_max"] == 200.0
