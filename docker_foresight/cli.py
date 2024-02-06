
import argparse
import pathlib
from dataclasses import dataclass


@dataclass(frozen=True)
class Arguments:
    file: pathlib.Path
    threshold: int | None

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to a Dockerfile",type=pathlib.Path,)
    parser.add_argument("--threshold", help="Maximum change risk allowed, causes pass or fail", type=int, default=None)
    args = parser.parse_args()
    return Arguments(file=args.file, threshold=args.threshold)

def main():
    from docker_foresight.docker_foresight import DockerForesight
    args: Arguments = _parse_args()
    fore = DockerForesight(dockerfile_path=args.file)
    report, raw = fore.analyze()
    out = fore.render(report, raw)
    print(out)
    print()
    score_fmt = f"{report.score:.2f}"
    if args.threshold is not None:
        if report.score > args.threshold:
            print(f"FAILURE: Score {score_fmt} is greater than threshold of {args.threshold}")
            exit(1)
        print(f"SUCCESS: Score {report.score} is within threshold of {args.threshold}")

if __name__=="__main__":
    print("abc")
    main()
    print("Done")

