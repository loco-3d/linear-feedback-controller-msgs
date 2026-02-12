# This is a message that holds data to describe the control computed by an optimal controller.
#
# The message contains:
# - a classical ROS header
# - the linear feedback gain matrix, a.k.a. the Ricatti (LQR equivalent) gain matrix.
# - the feedforward vector, in this case the joitn torques usually.
# - the initial state of the system, the Sensor message used as initial state for the optimal control problem.
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
