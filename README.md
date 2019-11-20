# gammapy-config

- Explore config handling options for Gammapy.
- José Enrique Ruiz & Christoph Deil
- Nov 19, 2019

## What is this?

Our goal is to make a decision how to do config handling
for the Analysis class in Gammapy. Our goal is not to
find the solution for models, that might or might not
be the same.

See https://github.com/gammapy/gammapy/issues/401

## Conclusion

- We recommend to replace `python-jsonschema` dependency by something new 
- Effort: approx 1 day coding and 1-2 time to improve documentation
- We recommend to use: **TBD**

## Requirements and wishes

- Support hierarchical config (`general.logging.level`)
- Support to and from dict / JSON / YAML 
- Property dot access and tab completion for getting & setting
- Nice representation of overall config and specific settings
- Support for config update with a file or dict as in dict.update()
- Validation for python and custom types at init and setting:
    - regexp (short syntax for complex params)
    - astropy quantities and angles / type casting
    - dependencies and required values
- Support "frozen" config to guard against mistyping,
  i.e. `config.something = "spam"` will raise an error
  if `config.something` isn't defined in the config 
- Good error messages

## Options

We considered the following options:

- [pydantic](https://github.com/samuelcolvin/pydantic) - [config_pydantic.py](config_pydantic.py) - [test_config_pydantic.py](config_pydantic.py) 
- [traitlets](https://traitlets.readthedocs.io/) - [config_traitlets.py](config_traitlets.py)
- [astropy.config](http://docs.astropy.org/en/stable/config/index.html) - [config_astropy.py](config_astropy.py) 
- [configurator](https://configurator.readthedocs.io) - no prototype
- [attrs](http://www.attrs.org/) - no prototype
- [dataclasses-jsonschema](https://github.com/s-knibbs/dataclasses-jsonschema) - no prototype
- [python-jsonchema-objects](https://github.com/cwacek/python-jsonschema-objects) - no prototype
- [marshmallow](https://github.com/marshmallow-code/marshmallow) - no prototype
- [warlock](https://github.com/bcwaldon/warlock) - no prototype
- [anyconfig](https://github.com/ssato/python-anyconfig) - no prototype
- [python-box](https://github.com/cdgriffith/Box) - no prototype
- [lsst/pex_config](https://github.com/lsst/pex_config) - no prototype

|              | Hierarchical | YAML/JSON |   Dot  |  Repr  | Update | Typed | Frozen | Messages |
| :----------: | :----------: | :-------: | :----: | :----: | :----: | :---: | :----: | :------: |
| current      |      o       |     o     |    x   |    c   |    c   |   i   |    o   |    o     |
| pydantic     |      o       |     o     |    o   |    o   |    x   |   o   |    o   |    o     |

- o: ok
- c: custom devel
- i: on init

## Syntax for configuration settings

- [Proposed example file](example-config.yaml)
- [Existing options](docs.yaml)
- [Template basic](template-basic.yaml)
- [Template 1D](template-1d.yaml)
- [Template 3D](template-3d.yaml)

## Notes

- https://github.com/s-knibbs/dataclasses-jsonschema/issues/117
