# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- dont try to publish the release on github twice

## [0.12.2] - 2026-10-21

- fix release

## [0.12.1] - 2026-10-21

- `mkdir -p site-packages`

## [0.12.0] - 2026-10-20

## [0.11.1] - 2026-07-16

- improve error message whe "tag_name" is not available
- fix lock

## [0.11.0] - 2026-07-15

- don't get latest github release when `version` is set

## [0.10.1] - 2026-07-13

- fix release

## [0.10.0] - 2026-07-13

- github: add 20s timeout

## [0.9.0] - 2026-07-03

- set `WORKDIR` to `/dockgen` instead of `/src`
- set `CMAKE_INSTALL_PREFIX=/usr/local`

## [0.8.0] - 2026-05-28

- added `pip_deps` support. use with care.
  dont mix apt & pip unless your absolutely sure what you do.

## [0.7.1] - 2026-04-14

## [0.7.0] - 2026-04-14

- fix project order

## [0.6.1] - 2026-03-07

- allow uv_build 0.10

## [0.6.0] - 2025-11-20

## [0.5.0] - 2025-10-20

- add `ca-certificates` apt package
- allow uv_build v0.9
- update tests for jrl-cmakemodules #790

## [0.4.0] - 2025-09-30

- add `configure_args` option
- setup dependabot uv

## [0.3.0] - 2025-07-28

- use upstream for eigenpy online test
- hatchling -> uv_build

## [0.2.0] - 2025-07-16

- Add changelog
- Setup release process

## [0.1.0] - 2025-07-16

- Initial minial working version

[Unreleased]: https://github.com/nim65s/dockgen/compare/v0.11.1...main
[0.11.1]: https://github.com/nim65s/dockgen/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/nim65s/dockgen/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/nim65s/dockgen/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/nim65s/dockgen/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/nim65s/dockgen/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/nim65s/dockgen/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/nim65s/dockgen/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/nim65s/dockgen/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/nim65s/dockgen/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/nim65s/dockgen/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/nim65s/dockgen/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/nim65s/dockgen/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/nim65s/dockgen/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/nim65s/dockgen/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/nim65s/dockgen/releases/tag/v0.1.0
