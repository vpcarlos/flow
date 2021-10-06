# Flow
Useful CLI to improve git flow


## Requirements
Python 3.9+
poetry
git-flow

## Instalation
For now is instable with poetry, future version will be install by `pip`.
```console
$ cd flow
$ poetry install
$ poetry shell
```

## Usage

Flow works with a new `git-flow` repository or and older one.
We have change flow mind, now main commads are `start`, `publish` and `finish`.

### Creating a new git flow repo
```console
$ git flow init 
```
### Starting
#### Feature
```console
$ flow start feature my-magic-feature
```
#### Release
```console
$ flow start release [major|minor|patch]
```
This command will fetch all your relases, take the last one and compute the next one.

### Publishing
#### Feature or Release
```console
$ flow publish
```
You don't need to specify what you want to publish, we take that information from current branch and gitflow configuration.

### Finishing
#### Feature or Release
```console
$ flow finish
```
You don't need to specify what you want to finish, we take that information from current branch and gitflow configuration.




