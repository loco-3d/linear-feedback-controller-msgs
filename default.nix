{
  lib,
  stdenv,
  cmake,
  eigen,
  python3Packages,
  rosPackages,
}:
stdenv.mkDerivation {
  pname = "linear-feedback-controller-msgs";
  version = "0.1.3";

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./CMakeLists.txt
      ./include
      ./linear_feedback_controller_msgs_py
      ./msg
      ./package.xml
      ./tests
    ];
  };

  nativeBuildInputs = [
    cmake
    eigen
    python3Packages.python
    rosPackages.jazzy.ament-cmake
    rosPackages.jazzy.ament-cmake-cppcheck
    rosPackages.jazzy.ament-cmake-cpplint
    rosPackages.jazzy.ament-cmake-flake8
    rosPackages.jazzy.ament-cmake-pep257
    rosPackages.jazzy.ament-cmake-uncrustify
    rosPackages.jazzy.rosidl-default-generators
  ];

  propagatedBuildInputs = [
    rosPackages.jazzy.geometry-msgs
    rosPackages.jazzy.sensor-msgs
    rosPackages.jazzy.tf2-eigen
  ];

  doCheck = true;

  meta = {
    description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";
    homepage = "https://github.com/loco-3d/linear-feedback-controller-msgs";
    license = lib.licenses.bsd2;
    maintainers = [ lib.maintainers.nim65s ];
    platforms = lib.platforms.linux;
  };
}
