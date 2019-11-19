"""Try Gammapy config with astropy.config."""
from astropy.config import ConfigNamespace, ConfigItem

class LoggingConfig(ConfigNamespace):
    level = ConfigItem()
    filename = ConfigItem()

class ObservationConfig(ConfigNamespace):
    c1 = ConfigItem(cfgtype="int")
    c2 = ConfigItem(cfgtype="float")
    c3 = ConfigItem(cfgtype="string")

    log = LoggingConfig()

if __name__ == '__main__':
    c = ObservationConfig()
    print(c)
    print(c.c1)
    print(c.log)
    print(c.log.level)
    print(c.__dict__)
