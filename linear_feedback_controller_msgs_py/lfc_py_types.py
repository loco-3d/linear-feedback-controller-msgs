from typing import Annotated, List, Literal
from dataclasses import dataclass
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

    name: List[str]
    position: npt.NDArray[np.float64]
    velocity: npt.NDArray[np.float64]
    effort: npt.NDArray[np.float64]
    stamp: Time


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
    contacts: List[Contact]


@dataclass
class Control:
    """Structure containing Control information similarly to ROS message
    linear_feedback_controller_msgs.msg.Control.
    """

    feedback_gain: npt.NDArray[np.float64]
    feedforward: npt.NDArray[np.float64]
    initial_state: Sensor
