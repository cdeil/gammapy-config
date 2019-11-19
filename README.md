# gammapy-config

- Explore config handling options for Gammapy.
- José-Enrique Ruiz & Christoph Deil
- Nov 19, 2019

## What is this?

Our goal is to make a decision how to do config handling
for the Analysis class in Gammapy. Our goal is not to
find the solution for models, that might or might not
be the same.

See https://github.com/gammapy/gammapy/issues/401

## Conclusion

- We recommend to change to something new
- Effort: approx 1 day coding and 1-2 time to improve documentation
- We recommend to use: **TBD**

## Requirements and wishes

- Support hierarchical config (`general.logging.level`)
- Need to support lists?
- Support to and from dict / JSON / YAML
- Good error messages
- Property dot access and tab completion for getting & setting
- Type validation at least, also some type casting?
- Option to create "frozen" config to guard against mistyping,
  i.e. `config.something = "spam"` will raise an error
  if `config.something` isn't defined in the config

## Options

We considered the following options:

- [pydantic](https://github.com/samuelcolvin/pydantic) - [config_pydantic.py](config_pydantic.py) 
- [traitlets](https://traitlets.readthedocs.io/) - [config_traitlets.py](config_traitlets.py)
- [astropy.config](http://docs.astropy.org/en/stable/config/index.html) - [config_astropy.py](config_astropy.py) 
- [dataclasses-jsonschema](https://github.com/s-knibbs/dataclasses-jsonschema) - no prototype
- [marshmallow](https://github.com/marshmallow-code/marshmallow) - no prototype

## Notes

- https://github.com/s-knibbs/dataclasses-jsonschema/issues/117
