from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = 1

Game = Literal["gt7", "ac", "other"]
SessionMode = Literal["hotlap", "practice", "race"]
Weather = Literal["dry", "wet", "mixed", "unknown"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class AppInfo(StrictModel):
    name: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=50)
    parser_version: str = Field(min_length=1, max_length=50)


class CarRef(StrictModel):
    game_car_id: Annotated[int | str, Field(description="ID do carro no jogo")]
    name: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=100)


class TrackRef(StrictModel):
    game_track_id: Annotated[int | str, Field(description="ID da pista no jogo")]
    name: str | None = Field(default=None, max_length=200)
    length_m: float | None = Field(default=None, gt=0)


class Conditions(StrictModel):
    air_temp_c: float | None = Field(default=None, ge=-50, le=70)
    track_temp_c: float | None = Field(default=None, ge=-50, le=100)
    weather: Weather = "unknown"
    track_wetness_pct: float | None = Field(default=None, ge=0, le=100)
    time_of_day: str | None = Field(default=None, max_length=50)


class Rules(StrictModel):
    tire_wear_enabled: bool = False
    tire_wear_multiplier: float = Field(default=1.0, ge=0, le=20)
    fuel_consumption_enabled: bool = False
    fuel_consumption_multiplier: float = Field(default=1.0, ge=0, le=20)
    bop_enabled: bool | None = None
    tuning_allowed: bool | None = None
    pp_limit: float | None = Field(default=None, gt=0)


class TireState(StrictModel):
    compound: str | None = Field(default=None, max_length=100)
    age_laps_start: int = Field(default=0, ge=0)
    wear_pct_start: float | None = Field(default=None, ge=0, le=100)


class FuelState(StrictModel):
    start_l: float | None = Field(default=None, ge=0)
    capacity_l: float | None = Field(default=None, gt=0)
    density_kg_l: float = Field(default=0.75, gt=0, le=1.5)


class LapTire(StrictModel):
    age_laps: int | None = Field(default=None, ge=0)
    wear_pct_start: float | None = Field(default=None, ge=0, le=100)
    wear_pct_end: float | None = Field(default=None, ge=0, le=100)


class LapFuel(StrictModel):
    start_l: float | None = Field(default=None, ge=0)
    end_l: float | None = Field(default=None, ge=0)
    used_l: float | None = Field(default=None, ge=0)


class LapStats(StrictModel):
    max_speed_kmh: float | None = Field(default=None, ge=0)
    min_speed_kmh: float | None = Field(default=None, ge=0)
    avg_speed_kmh: float | None = Field(default=None, ge=0)
    avg_throttle_pct: float | None = Field(default=None, ge=0, le=100)
    avg_brake_pct: float | None = Field(default=None, ge=0, le=100)
    max_rpm: float | None = Field(default=None, ge=0)
    total_frames: int | None = Field(default=None, ge=0)


class Frame(StrictModel):
    seq: int = Field(ge=0)
    ts: float = Field(ge=0, description="Timestamp em segundos")
    speed_mps: float = Field(ge=0)
    throttle: float = Field(ge=0, le=255)
    brake: float = Field(ge=0, le=255)
    engine_rpm: float = Field(ge=0)
    gear: int = Field(ge=-1, le=20)
    position_x: float
    position_y: float
    position_z: float
    velocity_x: float | None = None
    velocity_y: float | None = None
    velocity_z: float | None = None
    tire_temp_fl: float | None = None
    tire_temp_fr: float | None = None
    tire_temp_rl: float | None = None
    tire_temp_rr: float | None = None
    suspension_fl: float | None = None
    suspension_fr: float | None = None
    suspension_rl: float | None = None
    suspension_rr: float | None = None
    fuel_level_l: float | None = Field(default=None, ge=0)
    steering: float | None = None


class Lap(StrictModel):
    number: int = Field(ge=0)
    lap_time_ms: int = Field(gt=0)
    sectors_ms: list[int] | None = Field(default=None, min_length=3, max_length=3)
    started_at: datetime | None = None
    is_outlap: bool = False
    is_inlap: bool = False
    is_valid: bool = True
    invalid_reason: str | None = Field(default=None, max_length=200)
    external_id: str | None = Field(default=None, max_length=200)
    notes: str | None = None
    tire: LapTire | None = None
    fuel: LapFuel | None = None
    conditions: Conditions | None = None
    stats: LapStats | None = None
    frames: list[Frame] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_sectors_and_frames(self) -> Lap:
        if self.sectors_ms is not None:
            if any(value < 0 for value in self.sectors_ms):
                raise ValueError("sectors_ms must contain only non-negative values")
        if self.frames:
            seqs = [frame.seq for frame in self.frames]
            if len(seqs) != len(set(seqs)):
                raise ValueError("frame seq values must be unique within a lap")
        if self.is_valid and self.invalid_reason:
            raise ValueError("invalid_reason requires is_valid=false")
        if not self.is_valid and not self.invalid_reason:
            raise ValueError("invalid_reason is required when is_valid=false")
        return self


class PositionSample(StrictModel):
    ts: float = Field(ge=0)
    position_x: float
    position_z: float
    lap_distance_m: float | None = Field(default=None, ge=0)


class OtherCar(StrictModel):
    external_id: str = Field(min_length=1, max_length=200)
    name: str | None = Field(default=None, max_length=200)
    game_car_id: Annotated[int | str, Field(default=None)]
    positions: list[PositionSample] = Field(default_factory=list)


class Session(StrictModel):
    game: Game
    mode: SessionMode
    started_at: datetime
    ended_at: datetime | None = None
    car: CarRef
    track: TrackRef
    setup_id: str | None = Field(default=None, max_length=200)
    setup_hash: str | None = Field(default=None, min_length=64, max_length=64)
    conditions: Conditions = Field(default_factory=Conditions)
    rules: Rules = Field(default_factory=Rules)
    tire: TireState = Field(default_factory=TireState)
    fuel: FuelState = Field(default_factory=FuelState)
    assists: dict[str, bool] = Field(default_factory=dict)
    notes: str | None = None
    other_cars: list[OtherCar] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_range(self) -> Session:
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise ValueError("ended_at must be greater than or equal to started_at")
        return self


class TelemetryBundle(StrictModel):
    schema_version: Literal[1] = SCHEMA_VERSION
    app: AppInfo
    session: Session
    laps: list[Lap] = Field(default_factory=list)
    created_at: datetime
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
