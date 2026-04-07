{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs = {
    gepetto.url = "github:gepetto/nix";
    flake-parts.follows = "gepetto/flake-parts";
    systems.follows = "gepetto/systems";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gepetto.flakeModule
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
