# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Releases are available on the [github repository](https://github.com/loco-3d/linear-feedback-controller-msgs/releases).

## [Unreleased]

## [1.0.0] - 2025-11-04

- Use the branch main as the unique branch.

- Add the dependency to jrl-cmakemodules
- Changed and upgrade the CI using Nix and ros-github-actions
- Fix typo in CMakeLists.txt

## [1.0.0] - 2025-04-11

- Changed the code to be comptible with ROS2
- Added Nix CI
- Fix Licensing removing an old header from PAL-ROBOTICS that do not apply anymore.
  PAL is included in the official BSD-2-clause license.

## [0.1.3] - 2023-04-18

- Added a CI

## [0.1.2] - 2023-04-03

- Changed and improve the packaging
- Added contact pose to the messages
- Added contacts state eigen conversion
- Added more unit-tests

## [0.1.1] - 2023-03-21

- Added unittests for the message generation and good behavior in the ROS eco-system.

## [0.1.0] - 2023-03-17

Implementation of linear-feedback-controller-msgs in ROS1 for Talos PAL-Robotics robot.
This ROS1 message package is meant for the
[linear-feedback-controller](https://github.com/loco-3d/linear-feedback-controller)
package.

## Git changelogs

[Unreleased]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v0.1.3...v1.0.0
[0.1.3]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/loco-3d/linear-feedback-controller-msgs/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/loco-3d/linear-feedback-controller-msgs/releases/tag/v0.1.0
