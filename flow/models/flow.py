from __future__ import annotations
import os
import git
import typer

from git import Git, Repo
from flow.constants import TYPES, FLOW
from typing import Optional


class Flow():

    @staticmethod
    def get_config(key: str) -> Optional[str]:
        """Get git configuration by key."""
        try:
            g = Git()
            res = g.config('--get', key)
        except git.exc.GitCommandError:
            res = None
            typer.echo(f'Config: {key} not found')
        return res

    @classmethod
    def git_flow(cls, command: str, branch: str) -> bool:
        """ Execute git flow command."""
        error = os.system(
            f'git flow {cls.__name__.lower()} {command} {branch}')
        return not error

    @classmethod
    def get_flow_prefix(cls, flow: str = '') -> Optional[str]:
        """ Get a setted prefix from git flow"""
        key = f'gitflow.prefix.{flow or cls.__name__.lower()}'
        return cls.get_config(key)

    @classmethod
    def get_new_pr_url(cls) -> str:
        """ Create a new PR url."""
        g = Git()
        remote_url = str(g.config('remote.origin.url', get=True))
        is_ssh = remote_url.startswith('git@')
        work_branch = cls.get_config(f'gitflow.branch.{cls._env}')
        _branch = cls.get_active_branch()

        if is_ssh:
            remote_url = remote_url.replace(
                ':', '/', 1).replace('git@', 'https://', 1)
        new_pr_url = remote_url.replace(
            '.git', f'/compare/{work_branch}...{_branch}?expand=1', 1)
        return new_pr_url

    @classmethod
    def get_flow_branch(cls) -> Optional[str]:
        """Get branch name without git flow prefix."""
        prefix = cls.get_flow_prefix()
        if prefix:
            branch = cls.get_active_branch()
            return str(branch).replace(prefix, '', 1)

    @staticmethod
    def get_active_branch() -> str:
        """Get entire current branch name."""
        repo = Repo.init()
        return repo.active_branch

    @classmethod
    def factory(cls) -> Optional[Flow]:
        """Check current branch and instance a Flow child depending on prefix."""
        active_branch = cls.get_active_branch()
        for f in FLOW:
            flow_prefix = cls.get_flow_prefix(f)
            if str(active_branch).startswith(flow_prefix):
                for subclass in cls.__subclasses__():
                    if subclass.__name__.lower() == f:
                        return subclass


class Feature(Flow):
    _env: str = 'develop'


class Release(Flow):
    _env: str = 'master'

    @staticmethod
    def last_release() -> str:
        """ Get the last release from the main branch."""
        g = Git()
        work_branch = Release.get_config('gitflow.branch.master')
        g.checkout(work_branch)
        typer.secho('Fetching tags...', fg=typer.colors.GREEN)
        g.fetch('--tags', '--all')
        last_version = g.describe('--abbrev=0')
        typer.secho(
            f'Last version found --> {last_version}', fg=typer.colors.GREEN)
        return last_version

    @staticmethod
    def build_next(version_type: str) -> str:
        """ Build the lnext release version."""
        # Get last git release
        last_release = Release.last_release()

        # Parse version format, this will help us to handle version with numbers:
        # Ex. 'v3.5.1'(str) --> [3, 5, 1] (List[int])
        # Ex. 'v0-8-1'(str) --> [0, 8, 1] (List[int])
        separator = '-' if '-' in last_release else '.'
        release_prefix = Release.get_config('gitflow.prefix.versiontag')
        last_release = last_release.replace(release_prefix, '', 1)
        version = list(map(int, last_release.split(separator)))

        # Add a 1 to the current version_type and fill the rest with 0
        # Ex. 'patch' --> parse [3, 5, 1] to [3, 5, 2]
        # Ex. 'minor' --> parse [3, 5, 1] to [3, 6, 0]
        # Ex. 'major' --> parse [3, 5, 1] to [4, 0, 0]
        version[TYPES[version_type]] += 1
        num_zeros = (2 - TYPES[version_type])
        version[TYPES[version_type]+1:] = [0] * num_zeros

        # Format the new version adding the prefix and separator
        next_version = release_prefix + separator.join(list(map(str, version)))
        typer.secho(f'New version --> {next_version}', fg=typer.colors.GREEN)
        return next_version


class Hotfix(Flow):
    pass
