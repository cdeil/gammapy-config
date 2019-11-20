"""Try Gammapy config with pydantic."""
from typing import List
import yaml
from astropy.time import Time
from astropy.coordinates import Angle
from pydantic import BaseModel

class PyDanticConfig:
    validate_assignment = True
    extra = "forbid"
    # arbitrary_types_allowed = False


class AngleType(Angle):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return Angle(v)

class TimeType(Time):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, Time):
            return v
        elif isinstance(v, str):
            start, stop = v.split(" - ")
            return Time([start, stop])
        else:
            raise ValueError()

class LoggingConfig(BaseModel):
    level = "info"
    filename: str = None

    Config = PyDanticConfig

class GeneralConfig(BaseModel):
    log = LoggingConfig()
    outdir = "."

    Config = PyDanticConfig


class AnalysisConfig(BaseModel):
    general = GeneralConfig()

    c1: int = 42
    c2: float = 99.9
    c3: str = "spam"
    a: AngleType = "99 deg"
    time: TimeType = None

    obs_ids: List[int] = None

    Config = PyDanticConfig

    def to_yaml(self):
        return yaml.dump(self.dict())
