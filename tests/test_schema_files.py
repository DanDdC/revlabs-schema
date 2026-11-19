import json
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schema" / "v1"
EXAMPLES = ROOT / "examples"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_telemetry_json_schema_accepts_examples() -> None:
    schema = load(SCHEMAS / "telemetry.schema.json")
    for name in ("telemetry_hotlap.json", "telemetry_race.json"):
        validate(instance=load(EXAMPLES / name), schema=schema)


def test_track_geometry_json_schema_accepts_example() -> None:
    schema = load(SCHEMAS / "track-geometry.schema.json")
    validate(instance=load(EXAMPLES / "track_interlagos.json"), schema=schema)
