import astropy.units as u
from gammapy.time import Time
from astropy.coordinates import Angle, SkyCoord
from .config_pydantic import AnalysisConfig


if __name__ == '__main__':
    c = AnalysisConfig()
    print(c)
    print(repr(c))
    print(c.c1)
    print(c.log)
    print(c.log.level)

    print(c.a)
    c.a = "42 deg"
    assert isinstance(c.a, Angle)

    c.c1 = 1234
    # c.hombre = "enrique"
    # c.a = "99 deg"
    print(c.a)
