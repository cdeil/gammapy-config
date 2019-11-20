"""Try Gammapy config with pydantic."""
from astropy.coordinates import Angle
from pydantic import BaseModel

class AngleType(Angle):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return Angle(v)

class LoggingConfig(BaseModel):
    level = "info"
    filename: str = None

class GeneralConfig(BaseModel):
    log: LoggingConfig = LoggingConfig()
    outdir = "."

class AnalysisConfig(BaseModel):
    general: GeneralConfig

    c1: int = 42
    c2: float = 99.9
    c3: str = "spam"
    a: AngleType = "99 deg"

    class Config:
        validate_assignment = True
        # arbitrary_types_allowed = True
