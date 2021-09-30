import os


class Flow():

    @classmethod
    def command(cls, command: str, branch: str) -> bool:
        error = os.system(
            f'git flow {cls.__name__.lower()} {command} {branch}')
        return not error

    @classmethod
    def get_flow_branch(cls):
        error = os.system(
            f'git config --get gitflow.prefix.{cls.__name__.lower()}')


class Feature(Flow):
    pass


class Hotfix(Flow):
    pass


class Support(Flow):
    pass
