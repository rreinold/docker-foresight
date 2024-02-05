import pytest

from docker_foresight.docker_foresight import DockerForesight, Report, Line


def test_docker_foresight():
    dfore = DockerForesight(dockerfile_path="Dockerfile")
    actual,_ = dfore.analyze()
    assert actual.score == 15.96875
