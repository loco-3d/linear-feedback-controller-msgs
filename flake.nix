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
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, self, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gepetto.flakeModule
          { gepetto-pkgs.overlays = [ self.overlays.default ]; }
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
            };
          };
        perSystem =
          { pkgs, ... }:
          {
            packages = lib.filterAttrs (_n: v: v.meta.available && !v.meta.broken) (rec {
              default = humble-linear-feedback-controller-msgs;
              humble-linear-feedback-controller-msgs = pkgs.rosPackages.humble.linear-feedback-controller-msgs;
              jazzy-linear-feedback-controller-msgs = pkgs.rosPackages.jazzy.linear-feedback-controller-msgs;
            });
          };
      }
    );
}
