{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs = {
    gepetto.url = "github:gepetto/nix";
    flake-parts.follows = "gepetto/flake-parts";
    nixpkgs.follows = "gepetto/nixpkgs";
    nix-ros-overlay.follows = "gepetto/nix-ros-overlay";
    treefmt-nix.follows = "gepetto/treefmt-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" ];
      imports = [ inputs.treefmt-nix.flakeModule ];
      perSystem =
        {
          lib,
          pkgs,
          system,
          self',
          ...
        }:
        {
          _module.args.pkgs = import inputs.nixpkgs {
            inherit system;
            overlays = [
              inputs.nix-ros-overlay.overlays.default
              inputs.gepetto.overlays.default
            ];
          };
          checks = lib.mapAttrs' (n: lib.nameValuePair "package-${n}") self'.packages;
          packages = let
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
            in {
              default = self'.packages.humble-linear-feedback-controller-msgs;
              humble-linear-feedback-controller-msgs =
                pkgs.rosPackages.humble.linear-feedback-controller-msgs.overrideAttrs { inherit src; };
              jazzy-linear-feedback-controller-msgs =
                pkgs.rosPackages.jazzy.linear-feedback-controller-msgs.overrideAttrs { inherit src; };
            };
          treefmt.programs = {
            deadnix.enable = true;
            nixfmt.enable = true;
          };
        };
    };
}
