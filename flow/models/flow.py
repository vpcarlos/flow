import os
import git
import typer
repo = git.Repo.init()


class Flow():

    @classmethod
    def command(cls, command: str, branch: str) -> bool:
        error = os.system(
            f'git flow {cls.__name__.lower()} {command} {branch}')
        return not error

    @classmethod
    def get_flow_prefix(cls):

        try:
            res = repo.git.config(
                '--get', f'gitflow.prefix.{cls.__name__.lower()}')
        except git.exc.GitCommandError:
            res = None
            typer.echo('git flow not initialized')

        return res
    
    @classmethod
    def get_flow_branch(cls):
        prefix = cls.get_flow_prefix()



class Feature(Flow):
    pass


class Hotfix(Flow):
    pass


class Support(Flow):
    pass
