from dataclasses import dataclass, field
from typing import Annotated, Literal

import numpy as np
import numpy.typing as npt
from rclpy.time import Time

np_array6 = Annotated[npt.NDArray[np.float64], Literal[6]]
np_array7 = Annotated[npt.NDArray[np.float64], Literal[7]]


@dataclass
class JointState:
    """Structure containing JointState information similarly to ROS message
    sensor_msgs.msg.JointState.
    """

    name: list[str]
    position: npt.NDArray[np.float64]
    velocity: npt.NDArray[np.float64]
    effort: npt.NDArray[np.float64]


@dataclass
class Contact:
    """Structure containing Contact information similarly to ROS message
    linear_feedback_controller_msgs.msg.Contact.
    """

    active: bool
    name: str
    wrench: np_array6
    pose: np_array7


@dataclass
class Sensor:
    """Structure containing Sensor information similarly to ROS message
    linear_feedback_controller_msgs.msg.Sensor.
    """

    base_pose: np_array7
    base_twist: np_array6
    joint_state: JointState
    contacts: list[Contact]
    stamp: Time = field(default_factory=Time)


@dataclass
class Control:
    """Structure containing Control information similarly to ROS message
    linear_feedback_controller_msgs.msg.Control.
    """

    feedback_gain: npt.NDArray[np.float64]
    feedforward: npt.NDArray[np.float64]
    initial_state: Sensor
    # Optional: the solution's state(s) after initial_state. Each element's own
    # .stamp is the time it applies at -- do not assume a fixed period between
    # elements, read the stamps. Empty when not used.
    next_states: list[Sensor] = field(default_factory=list)
    stamp: Time = field(default_factory=Time)
