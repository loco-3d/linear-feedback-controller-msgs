{
  description = "ROS messages which correspond to the loco-3d/linear-feedback-controller package.";

  inputs.gepetto.url = "github:gepetto/nix";

  outputs =
    inputs:
    inputs.gepetto.lib.mkFlakoboros inputs (
      { lib, ... }:
      {
        rosOverrideAttrs.linear-feedback-controller-msgs = {
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
    );
}
