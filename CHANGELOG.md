# Changelog for Zeusops bot

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project uses semantic versioning (see [semver](https://semver.org)).

## [Unreleased]

### Added

- New bot command `/current-mission` to show the currently active mission config.

## v0.3.1 - 2025-03-09

### Fixed

- `/zeus-list` command properly ignores `current-config.json` and `config.json`
- First item in mission list is now properly bulleted

## v0.3.0 - 2025-03-09

### Added

- New bot command `/zeus-list` to list all configured missions.

## v0.2.2 - 2025-03-09

### Fixed

- Calling `/zeus-set-mission` after an existing mission has already been set no
  longer crashes with `FileExistsError`.

## v0.2.1 - 2025-03-02

### Fixed

- Symlink for active mission created via `/zeus-set-mission` no longer point to
  the absolute path of the config, but relative to current folder. Fixes path
  issues when running inside containers (mismatching absolute paths)

## v0.2.0 - 2025-03-02

### Added

- CLI runs discord bot for reforger server config, exposed as slash-commands
  `/zeus-upload` and `/zeus-set-mission`
- New CI workflow for github, building the release-oriented docker image

## v0.1.0 - 2025-02-15

### Added

- New python module `zeusops_bot`, exposed as shell command `zeusops-bot`
