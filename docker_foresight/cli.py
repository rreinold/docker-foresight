
import argparse
import pathlib
from dataclasses import dataclass


@dataclass(frozen=True)
class Arguments:
    file: pathlib.Path

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to a Dockerfile",type=pathlib.Path,)
    args = parser.parse_args()
    return Arguments(file=args.file)

def main():
    print("ok")
    from docker_foresight.docker_foresight import DockerForesight
    args: Arguments = _parse_args()
    print(args.file)
    fore = DockerForesight(dockerfile_path=args.file)

if __name__=="__main__":
    print("abc")
    main()
    print("Done")

