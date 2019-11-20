"""Try Gammapy config with pydantic."""
from astropy.coordinates import Angle
import pydantic
from traitlets import TraitType, Unicode, Int, Float, List

class AngleTrait(TraitType):
    default_value = Angle("42 deg")
    info_text = 'An angle'

    def validate(self, obj, value):
        angle = Angle(value)
        return angle

class LoggingConfig(GammapyConfig):
    level = Unicode(help="Log level", default_value="info").tag(config=True)
    filename = Unicode(help="Log filename").tag(config=True)


class ObservationConfig(GammapyConfig):
    c1 = Int()
    c2 = Float()
    c3 = Unicode()
    a = AngleTrait()

    log = LoggingConfig()

    def from_json(self):
        return

if __name__ == '__main__':
    c = ObservationConfig()
    print(c)
    print(c.c1)
    print(c.log)
    print(c.log.level)
    print(c.a)

    c.c1 = 1234
    # c.hombre = "enrique"
    c.a = "99 deg"
    print(c.a)
