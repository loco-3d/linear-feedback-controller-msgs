# This is a message that holds data to describe the control computed by an optimal controller.
#
# The message contains:
# - a classical ROS header
# - the linear feedback gain matrix, a.k.a. the Ricatti (LQR equivalent) gain matrix.
# - the feedforward vector, in this case the joitn torques usually.
# - the initial state of the system, the Sensor message used as initial state for the optimal control problem.
# - optionally, the following state(s) of the optimal control problem's solution, for a controller that
#   interpolates its reference across the control period instead of holding it. Each state carries its own
#   header.stamp; consumers must derive the actual time offset from that stamp, not assume a fixed period.
#

# Metadata
##########

std_msgs/Header header

# Control data
##############

# Linear feedback gain matrix.
std_msgs/Float64MultiArray feedback_gain

# Vector of the feedforward.
std_msgs/Float64MultiArray feedforward

# Initial state
###############

Sensor initial_state

# Following states
##################

# The solution's state(s) after initial_state, each carrying its own
# header.stamp (the actual time it applies at -- do not assume a fixed period
# between elements, or between initial_state and next_states[0]; read the
# stamps). Optional: leave empty (default) when not used.
Sensor[] next_states
