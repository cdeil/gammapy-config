import pytest
import yaml
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import Angle, SkyCoord
from config_pydantic import AnalysisConfig


def test_config_basics():
    config = AnalysisConfig()
    config.a = "42 deg"
    assert isinstance(config.a, Angle)

    config.c1 = 1234

    config.obs_ids = [41, 42]
    assert config.obs_ids == [41, 42]

    config.time = "2019-12-01 - 2020-03-01"
    assert isinstance(config.time, Time)
    assert str(config.time[0]) == "2019-12-01 00:00:00.000"

def test_config_create_from_dict():
    data = yaml.safe_load(open("example-config.yaml"))
    # data = {"general": {"log": {"level": "warning"}}}
    config = AnalysisConfig(**data)
    assert config.general.log.level == "warning"

def test_config_to_yaml():
    config = AnalysisConfig()
    assert "filename: null" in config.to_yaml()

@pytest.mark.xfail(reason="TODO")
def test_config_update_from_dict():
    config = AnalysisConfig()
    # TODO: implement this. pydantic offers it? Or copy code from Gammapy?
    config.update_from_dict()

if __name__ == '__main__':
    test_config_basics()
    test_config_create_from_dict()
    test_config_update_from_dict()
