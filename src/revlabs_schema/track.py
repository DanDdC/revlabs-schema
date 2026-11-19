from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .telemetry import Game, TrackRef

SCHEMA_VERSION = 1


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Point(StrictModel):
    x: float
    y: float = 0.0
    z: float


class TrackPoint(StrictModel):
    x: float
    y: float = 0.0
    z: float
    distance_m: float = Field(ge=0)
    curvature: float | None = None


class Transform(StrictModel):
    rotation_deg: float = 0.0
    scale: float = Field(default=1.0, gt=0)
    offset_x: float = 0.0
    offset_z: float = 0.0


class TrackGeometry(StrictModel):
    schema_version: Literal[1] = SCHEMA_VERSION
    game: Game
    track: TrackRef
    version: int = Field(default=1, ge=1)
    source: Literal["telemetry", "manual", "osm"] = "telemetry"
    license: str = Field(default="original", max_length=100)
    length_m: float = Field(gt=0)
    closed: bool = True
    start_finish: TrackPoint
    sector_markers_m: Annotated[
        list[float],
        Field(
            default_factory=list,
            min_length=0,
            max_length=2,
            description="Distâncias acumuladas dos fins dos setores 1 e 2",
        ),
    ]
    points: list[TrackPoint] = Field(min_length=3)
    coordinate_system: str = Field(default="game", max_length=50)
    transform: Transform = Field(default_factory=Transform)
    svg_view_box: str | None = Field(default=None, max_length=100)
    svg_path: str | None = Field(default=None, max_length=200_000)
    created_at: datetime

    @model_validator(mode="after")
    def validate_geometry(self) -> TrackGeometry:
        if self.closed and self.points[0].distance_m != 0:
            raise ValueError("closed geometry must start at distance 0")
        if any(
            self.points[i].distance_m > self.points[i + 1].distance_m
            for i in range(len(self.points) - 1)
        ):
            raise ValueError("points must be ordered by distance_m")
        if self.sector_markers_m:
            if any(value <= 0 or value >= self.length_m for value in self.sector_markers_m):
                raise ValueError("sector markers must be between 0 and length_m")
            if self.sector_markers_m != sorted(self.sector_markers_m):
                raise ValueError("sector markers must be ordered")
        return self
