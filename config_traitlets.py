"""Try Gammapy config with traitlets."""
from astropy.coordinates import Angle
import traitlets.config
from traitlets import TraitType, Unicode, Int, Float, List
from gammapy.utils.scripts import make_path, read_yaml

CONFIG_FILE_YAML = "template-basic.yaml"
CONFIG_FILE_JSON = "template-basic.json"

# Support hierarchical config (general.logging.level)
# Support lists for composed observation filtering
# Property dot access and tab completion for getting & setting
# Nice representation of overall config and specific settings
# Support for config update with a file or dict as in dict.update()
# Validation for python and custom types at init and setting:
# regexp (short syntax for complex params)
# astropy quantities and angles
# dependencies and required values
# Support for type casting?
# Support "frozen" config to guard against mistyping, i.e. config.something = "spam" will raise an error if config.something isn't defined in the config
# Good error messages


class GammapyConfig(traitlets.config.Configurable):

    def __setattr__(self, key, value):
        # if key not in self.trait_names():
        #     raise ValueError("No hombre!")
        super().__setattr__(key, value)


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

    def from_dict(self):
        pass

    def from_json(self):
        pass

    def from_yaml(self):
        config = read_yaml(CONFIG_FILE)
        return config


if __name__ == '__main__':

    # Support to and from dict / JSON / YAML
    c = ObservationConfig().from_yaml()
    print(c)
    c = ObservationConfig().from_yaml()
    print(c)

    # print(c.c1)
    # print(c.log)
    # print(c.log.level)
    # print(c.a)
    #
    # c.c1 = 1234
    # # c.hombre = "enrique"
    # c.a = "99 deg"
    # print(c.a)

