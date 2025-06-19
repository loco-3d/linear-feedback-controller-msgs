{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs = {
    gepetto.url = "github:gepetto/nix";
    flake-parts.follows = "gepetto/flake-parts";
    nixpkgs.follows = "gepetto/nixpkgs";
    nix-ros-overlay.follows = "gepetto/nix-ros-overlay";
    systems.follows = "gepetto/systems";
    treefmt-nix.follows = "gepetto/treefmt-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = import inputs.systems;
      imports = [ inputs.gepetto.flakeModule ];
      perSystem =
        { lib, pkgs, ... }:
        {
          packages =
            let
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
            in
            lib.filterAttrs (_n: v: v.meta.available && !v.meta.broken) (rec {
              default = humble-linear-feedback-controller-msgs;
              humble-linear-feedback-controller-msgs =
                pkgs.rosPackages.humble.linear-feedback-controller-msgs.overrideAttrs
                  { inherit src; };
              jazzy-linear-feedback-controller-msgs =
                pkgs.rosPackages.jazzy.linear-feedback-controller-msgs.overrideAttrs
                  { inherit src; };
            });
        };
    };
}
