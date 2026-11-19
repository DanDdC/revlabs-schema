import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from revlabs_schema import TelemetryBundle, TrackGeometry

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_hotlap_example_is_valid() -> None:
    bundle = TelemetryBundle.model_validate(load("telemetry_hotlap.json"))
    assert bundle.schema_version == 1
    assert bundle.session.mode == "hotlap"
    assert bundle.laps[0].lap_time_ms == 97467


def test_race_example_is_valid() -> None:
    bundle = TelemetryBundle.model_validate(load("telemetry_race.json"))
    assert bundle.session.mode == "race"
    assert bundle.session.rules.tire_wear_multiplier == 2.0
    assert bundle.laps[1].fuel.used_l == 2.5


def test_missing_required_lap_time_fails() -> None:
    data = load("telemetry_hotlap.json")
    del data["laps"][0]["lap_time_ms"]
    with pytest.raises(ValidationError):
        TelemetryBundle.model_validate(data)


def test_sector_list_must_have_three_values() -> None:
    data = load("telemetry_hotlap.json")
    data["laps"][0]["sectors_ms"] = [1, 2]
    with pytest.raises(ValidationError):
        TelemetryBundle.model_validate(data)


def test_invalid_lap_requires_reason() -> None:
    data = load("telemetry_hotlap.json")
    data["laps"][0]["is_valid"] = False
    with pytest.raises(ValidationError):
        TelemetryBundle.model_validate(data)


def test_track_geometry_example_is_valid() -> None:
    geometry = TrackGeometry.model_validate(load("track_interlagos.json"))
    assert geometry.length_m == 100
    assert geometry.closed is True
    assert len(geometry.points) == 5


def test_track_points_must_be_ordered() -> None:
    data = load("track_interlagos.json")
    data["points"][1]["distance_m"] = 80
    with pytest.raises(ValidationError):
        TrackGeometry.model_validate(data)
