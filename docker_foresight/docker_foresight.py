import datetime
import logging
from enum import Enum

from dateutil.parser import parse
import dockerfile
import pathlib
from dataclasses import dataclass
import git

class Risk(str,Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass(frozen=True)
class Line:
    line_num: int
    change_rate: float

    @property
    def risk(self)->Risk:
        if self.change_rate < 4:
            return Risk.LOW
        if self.change_rate < 6:
            return Risk.MEDIUM
        return Risk.HIGH

@dataclass(frozen=True)
class Report:
    lines: list[Line]
    score: float

@dataclass(frozen=True)
class FileStats:
    num_changes:int = 0
    days_since_creation:int = 0



SUPPORTED_COMMANDS = ['COPY']

logger = logging.getLogger(__name__)

class DockerForesight():
    def __init__(self, dockerfile_path: pathlib.Path = "Dockerfile", git_root_path:pathlib.Path = ".", build_context:pathlib.Path = None):

        self.dockerfile_path = dockerfile_path
        self.build_context = build_context
        self.git_root_path = git_root_path

    @classmethod
    def get_supported_commands(cls, dockerfile:list[dockerfile.Command])->list[dockerfile.Command]:
        return [command for command in dockerfile if command.cmd in SUPPORTED_COMMANDS]


    @classmethod
    def calculate_rate(cls, stat:FileStats)->float:
        if not stat.days_since_creation or not stat.num_changes:
            return 0.0
        rate_per_month = (stat.num_changes / stat.days_since_creation) * 365
        return rate_per_month

    @classmethod
    def consolidate_line_stats(cls, stats: list[FileStats])->float:
        if len(stats) == 0:
            logger.error("Found invalid stats")
            return 0.0
        if len(stats) == 1:
            return cls.calculate_rate(stats[0])
        for s in stats:
            rates = [cls.calculate_rate(s) for s in stats]
            # assume no common commits
            return sum(rates)


    def analyze(self)->(Report, dict[int, str]):
        g = git.Git(self.git_root_path)
        dockerfile_parsed = dockerfile.parse_file(str(self.dockerfile_path))
        commands = self.get_supported_commands(dockerfile_parsed)
        dockerfile_by_line = self.get_dockerfile_by_line(dockerfile_parsed)
        report_lines = []
        for c in commands:
            input_files = c.value[0:-1]
            line_stats = []
            for f in input_files:
                # TODO consider common commits
                # TODO Add docker context dir
                logs = g.log('--reverse', '--pretty=format:"%ad"', "--date=format:%Y-%m-%d", f)
                log_lines = logs.split('\n')
                num_changes = len(log_lines)
                # TODO Remove
                log_lines[0] = "2023-01-01"
                # Oldest is first commit
                creation_date = parse(log_lines[0], fuzzy=True)
                # Should it be:
                #   1) file commits per unit of time (current impl)
                #   2) file commits per total commits
                days_since_creation = (datetime.datetime.now() - creation_date).days
                # support for months?
                stats = FileStats(num_changes=num_changes, days_since_creation=days_since_creation)
                line_stats.append(stats)
            change_rate = self.consolidate_line_stats(line_stats)
            line = Line(line_num=c.start_line, change_rate=change_rate)
            report_lines.append(line)
        score = self.calculate_score(report_lines, len(dockerfile_parsed))
        report = Report(lines=report_lines, score=score)
        return report, dockerfile_by_line

    @classmethod
    def render(cls, report:Report, dockerfile_by_line:dict[int, str])->str:
        lines = [f"Score: {round(report.score,2)}"]
        report_by_lines = {line.line_num: line for line in report.lines}
        for line_num,command in dockerfile_by_line.items():
            risk_fmted = "".ljust(8)
            if line_num in report_by_lines:
                risk = report_by_lines[line_num].risk
                risk_fmted = risk.ljust(8)
            out_line = f"{risk_fmted}{(str(line_num)).ljust(4)}: {command}"
            lines.append(out_line)
        return "\n".join(lines)

    @classmethod
    def get_dockerfile_by_line(cls, commands:list[dockerfile.Command])->dict[int, str]:
        return {command.start_line: command.original for command in commands}

    @classmethod
    def calculate_score(cls, line_stats, num_dockerfile_lines:int):
        return sum([l.change_rate for l in line_stats])/num_dockerfile_lines * 10