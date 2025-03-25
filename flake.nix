{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  # [2025/03/25] Target develop as main branch is too unstable for now.
  # Keep it until next release on jazzy.
  inputs.nix-ros-overlay.url = "github:lopsided98/nix-ros-overlay/develop";

  outputs =
    { nix-ros-overlay, self, ... }:
    nix-ros-overlay.inputs.flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nix-ros-overlay.inputs.nixpkgs {
          inherit system;
          overlays = [ nix-ros-overlay.overlays.default ];
        };
      in
      {
        packages = {
          default = self.packages.${system}.linear-feedback-controller-msgs-py;
          linear-feedback-controller-msgs = pkgs.callPackage ./default.nix { };
          linear-feedback-controller-msgs-py =
            pkgs.python3Packages.toPythonModule
              self.packages.${system}.linear-feedback-controller-msgs;
        };
      }
    );
}
