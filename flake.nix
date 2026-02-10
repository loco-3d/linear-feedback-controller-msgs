{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs = {
    gazebros2nix.url = "github:gepetto/gazebros2nix";
    flake-parts.follows = "gazebros2nix/flake-parts";
    nixpkgs.follows = "gazebros2nix/nixpkgs";
    nix-ros-overlay.follows = "gazebros2nix/nix-ros-overlay";
    systems.follows = "gazebros2nix/systems";
    treefmt-nix.follows = "gazebros2nix/treefmt-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, self, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gazebros2nix.flakeModule
          { gazebros2nix-pkgs.overlays = [ self.overlays.default ]; }
        ];
        flake.overlays.default =
          _final: prev:
          let
            scope = _ros-final: ros-prev: {
              linear-feedback-controller-msgs = ros-prev.linear-feedback-controller-msgs.overrideAttrs {
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
            };
          in
          {
            rosPackages = prev.rosPackages // {
              humble = prev.rosPackages.humble.overrideScope scope;
              jazzy = prev.rosPackages.jazzy.overrideScope scope;
              kilted = prev.rosPackages.kilted.overrideScope scope;
              rolling = prev.rosPackages.rolling.overrideScope scope;
            };
          };
        perSystem =
          { pkgs, ... }:
          {
            packages = lib.filterAttrs (_n: v: v.meta.available && !v.meta.broken) (rec {
              default = rolling-linear-feedback-controller-msgs;
              humble-linear-feedback-controller-msgs = pkgs.rosPackages.humble.linear-feedback-controller-msgs;
              jazzy-linear-feedback-controller-msgs = pkgs.rosPackages.jazzy.linear-feedback-controller-msgs;
              kilted-linear-feedback-controller-msgs = pkgs.rosPackages.kilted.linear-feedback-controller-msgs;
              rolling-linear-feedback-controller-msgs = pkgs.rosPackages.rolling.linear-feedback-controller-msgs;
            });
          };
      }
    );
}
