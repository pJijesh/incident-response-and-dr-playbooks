# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `tools/check_dr.py`: checks a BIA and restore test log against the tier rules (11 rules), with a generated gap report example and 40 tests.
- A worked-example restore test log for the fictional company, including a failed, a partial and an overdue test.
- Community health files: security policy, code of conduct, issue forms and a pull request template.
- Citation metadata (`CITATION.cff`) so the repository can be cited from GitHub.
- Dependabot configuration for GitHub Actions.

### Fixed

- Worked example: the HR system is now Tier 2 with a 24 hour RTO, because payroll (Tier 2) depends on it. The dependency map is redrawn.

## [1.0.0] - 2026-11-11

### Added

- First public release: UK-focused incident response and disaster recovery playbooks, templates and a tabletop exercise for small IT teams.
- See the README for scope, what has and has not been verified, and the roadmap.
