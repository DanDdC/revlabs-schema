from __future__ import annotations

import json
from pathlib import Path

from revlabs_schema import TelemetryBundle, TrackGeometry

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema" / "v1"


def main() -> None:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    schemas = {
        "telemetry.schema.json": TelemetryBundle.model_json_schema(),
        "track-geometry.schema.json": TrackGeometry.model_json_schema(),
    }
    for filename, schema in schemas.items():
        path = SCHEMA_DIR / filename
        path.write_text(
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
