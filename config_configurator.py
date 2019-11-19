"""Try Gammapy config with configurator."""
from astropy.coordinates import Angle
from configurator import Config
from voluptuous import Schema, All, Required, PathExists


if __name__ == '__main__':


    # Support to and from dict / JSON / YAML
    config = Config.from_path('template-basic.yaml')

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

    schema = Schema({
        'cache': {'location': All(str, PathExists()), 'max_files': int},
        'banner': Required(str),
        'threads': Required(int),
    })

    schema(config.data)

