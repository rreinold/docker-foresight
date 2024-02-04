import dockerfile
import pathlib

import git


class DockerForesight():
    def __init__(self, dockerfile_path: pathlib.Path = "Dockerfile", git_root_path:pathlib.Path = ".", build_context:pathlib.Path = None):

        self.dockerfile_path = dockerfile_path
        self.build_context = build_context
        self.git_root_path = git_root_path


    def analyze(self):
        g = git.Git(self.git_root_path)
        df_parsed = dockerfile.parse_file(self.dockerfile_path)
        copy_commands = [command for command in df_parsed if command.cmd == 'COPY']
        import datetime

        loginfo = g.log('--reverse', '--pretty=format:"%ad"', "--date=format:%Y-%m-%d", "pyproject.toml")
        log_lines = loginfo.split('\n')
        print(len(log_lines))
        from dateutil.parser import parse
        # TODO Match exact format
        oldest = parse(log_lines[0], fuzzy=True)
        today = datetime.datetime.now()
        (today - oldest).days

        all_commands = []
        for c in copy_commands:
            print(c)
            input_files = c.value[0:-1]
            print(input_files)
            rate_of_change = []
            for f in input_files:
                # TODO Add docker context dir
                logs = g.log('--reverse', '--pretty=format:"%ad"', "--date=format:%Y-%m-%d", f)
                log_lines = loginfo.split('\n')
                num_changes = len(log_lines)
                # TODO Remove
                log_lines[0] = "2023-01-01"
                creation_date = parse(log_lines[0], fuzzy=True)
                print(creation_date)
                days_since_creation = (datetime.datetime.now() - creation_date).days
                print("days old: ", days_since_creation)
                if not days_since_creation:
                    rate_of_change.append(0)
                    continue
                # support for months?
                rate_per_month = (num_changes / days_since_creation) * 30
                rate_of_change.append(rate_per_month)

            print(rate_of_change)
            all_commands.append(rate_of_change)
        return all_commands