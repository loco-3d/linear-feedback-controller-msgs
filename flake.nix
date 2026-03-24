{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs = {
    gazebros2nix.url = "github:gepetto/gazebros2nix";
    flakoboros.follows = "gazebros2nix/flakoboros";
    flake-parts.follows = "gazebros2nix/flake-parts";
    nixpkgs.follows = "gazebros2nix/nixpkgs";
    nix-ros-overlay.follows = "gazebros2nix/nix-ros-overlay";
    systems.follows = "gazebros2nix/systems";
    treefmt-nix.follows = "gazebros2nix/treefmt-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gazebros2nix.flakeModule
          {
            flakoboros.rosOverrideAttrs.linear-feedback-controller-msgs = _: _: {
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
            };
          }
        ];
      }
    );
}
