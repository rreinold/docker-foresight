import pytest

from docker_foresight.docker_foresight import DockerForesight, Report, Line


def test_docker_foresight():
    dfore = DockerForesight(dockerfile_path="Dockerfile")
    actual = dfore.analyze()
    print(actual)
    assert actual == Report(lines=[Line(line=14, change_rate=0.15075376884422112), Line(line=16, change_rate=0.2261306532663317)])
