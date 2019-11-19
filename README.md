# gammapy-config

Explore config handling options for Gammapy.

Goal is to make a decision how to do config handling
for the Analysis class in Gammapy. Our goal is not to
find the solution for models, that might or might not
be the same.

See https://github.com/gammapy/gammapy/issues/401

- Support hierarchical config (`general.logging.level`)
- Need to support lists?
- Support to and from dict / JSON / YAML
- Good error messages
- Property dot access and tab completion for getting & setting
- Type validation at least, also some type casting?
- Option to create "frozen" config to guard against mistyping,
  i.e. `config.something = "spam"` will raise an error
  if `config.something` isn't defined in the config


## Notes

- https://github.com/s-knibbs/dataclasses-jsonschema/issues/117
