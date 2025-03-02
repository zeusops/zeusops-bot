# Changelog for Zeusops bot

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project uses semantic versioning (see [semver](https://semver.org)).

## [Unreleased]

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
