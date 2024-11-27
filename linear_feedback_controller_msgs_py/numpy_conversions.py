import numpy as np
import numpy.typing as npt
from typing import Annotated, Literal

from std_msgs.msg import Float64MultiArray, MultiArrayDimension

from geometry_msgs.msg import Pose, Point, Quaternion, Twist, Vector3, Wrench
from sensor_msgs.msg import JointState

import linear_feedback_controller_msgs_py.lfc_py_types as lfc_py_types

from linear_feedback_controller_msgs.msg import Contact, Control, Sensor

np_array3 = Annotated[npt.NDArray[np.float64], Literal[3]]
np_array6 = Annotated[npt.NDArray[np.float64], Literal[6]]
np_array7 = Annotated[npt.NDArray[np.float64], Literal[7]]


def vector3_numpy_to_msg(input: np_array3) -> Vector3:
    """Converts Numpy array of shape (3,) to ROS Vector3 message.
    Expected order of axes is (x, y, z).

    Args:
        input (npt.NDArray[np.float64], Literal[3]): Input vector as Numpy array.

    Returns:
        geometry_msgs.msg.Vector3: Vector represented as a ROS message.
    """
    assert (
        input.ndim == 1
    ), f"Input vector has '{input.ndim}' dimensions, expected dimension size of 1!"
    assert (
        input.size == 3
    ), f"Input vector has length of '{input.size}', expected length '3'!"
    return Vector3(x=input[0], y=input[1], z=input[2])


def pose_numpy_to_msg(input: np_array7) -> Pose:
    """Converts Numpy array of shape (7,) to ROS Pose message.
    Expected order of axes is (position.x, position.y, position.z, orientation.x,
    orientation.y, orientation.z, orientation.w).

    Args:
        input (npt.NDArray[np.float64], Literal[7]): Input pose as Numpy array.

    Returns:
        geometry_msgs.msg.Pose: Pose represented as a ROS message.
    """
    assert (
        input.ndim == 1
    ), f"Input vector has '{input.ndim}' dimensions, expected dimension size of 1"
    assert (
        input.size == 7
    ), f"Input vector has length of '{input.size}', expected length '7'!"
    return Pose(
        position=Point(x=input[0], y=input[1], z=input[2]),
        orientation=Quaternion(x=input[3], y=input[4], z=input[5], w=input[6]),
    )


def wrench_numpy_to_msg(input: np_array6) -> Wrench:
    """Converts Numpy array of shape (6,) to ROS Wrench message.
    Expected order of axes is (force.x, force.y, force.z, torque.x,
    torque.y, torque.z).

    Args:
        input (npt.NDArray[np.float64], Literal[6]): Input wrench as Numpy array.

    Returns:
        geometry_msgs.msg.Wrench: Wrench represented as a ROS message.
    """
    assert (
        input.ndim == 1
    ), f"Input vector has '{input.ndim}' dimensions, expected dimension size of 1"
    assert (
        input.size == 6
    ), f"Input vector has length of '{input.size}', expected length '6'!"
    return Wrench(
        force=vector3_numpy_to_msg(input[:3]),
        torque=vector3_numpy_to_msg(input[3:]),
    )


def twist_numpy_to_msg(input: np_array6) -> Twist:
    """Converts Numpy array of shape (6,) to ROS Twist message.
    Expected order of axes is (linear.x, linear.y, linear.z, angular.x,
    angular.y, angular.z).

    Args:
        input (npt.NDArray[np.float64], Literal[6]): Input twist as Numpy array.

    Returns:
        geometry_msgs.msg.Twist: Twist represented as a ROS message.
    """
    assert (
        input.ndim == 1
    ), f"Input vector has '{input.ndim}' dimensions, expected dimension size of 1"
    assert (
        input.size == 6
    ), f"Input vector has length of '{input.size}', expected length ''6!"
    return Twist(
        linear=vector3_numpy_to_msg(input[:3]),
        angular=vector3_numpy_to_msg(input[3:]),
    )


def pose_msg_to_numpy(msg: Pose) -> np_array7:
    """Converts ROS Pose message into Numpy array of shape (7,).
    Output order is (position.x, position.y, position.z, orientation.x,
    orientation.y, orientation.z, orientation.w).

    Args:
        msg (geometry_msgs.msg.Pose): Input ROS Pose message.

    Returns:
        npt.NDArray[np.float64], Literal[7]: Numpy array of shape (7,)
        with position and orientation vectors concatenated.
    """
    return np.array(
        [
            msg.position.x,
            msg.position.y,
            msg.position.z,
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w,
        ]
    )


def wrench_msg_to_numpy(msg: Wrench) -> np_array6:
    """Converts ROS Wrench message into Numpy array of shape (6,).
    Output order is (force.x, force.y, force.z, torque.x, torque.y, torque.z).

    Args:
        msg (geometry_msgs.msg.Wrench): Input ROS Wrench message.

    Returns:
        npt.NDArray[np.float64], Literal[6]: Numpy array of shape (6,)
        with force and torque vector concatenated.
    """
    return np.array(
        [
            msg.force.x,
            msg.force.y,
            msg.force.z,
            msg.torque.x,
            msg.torque.y,
            msg.torque.z,
        ]
    )


def twist_msg_to_numpy(msg: Twist) -> np_array6:
    """Converts ROS Twist message into Numpy array of shape (6,).
    Output order is (linear.x, linear.y, linear.z, angular.x,
    angular.y, angular.z).

    Args:
        msg (geometry_msgs.msg.Pose): Input ROS Twist message.

    Returns:
        npt.NDArray[np.float64], Literal[6]: Numpy array of shape (6,)
        with linear and angular vectors concatenated.
    """
    return np.array(
        [
            msg.linear.x,
            msg.linear.y,
            msg.linear.z,
            msg.angular.x,
            msg.angular.y,
            msg.angular.z,
        ]
    )


def matrix_numpy_to_msg(input: npt.NDArray[np.float64]) -> Float64MultiArray:
    """Converts Numpy array into ROS array message.

    Args:
        input (npt.NDArray[np.float64]]): Input matrix of size (N,2) or (N,).

    Returns:
        std_msgs.msg.Float64MultiArray: ROS message with the matrix.
    """
    # In case vector is passed consider is (N,1) array.
    rows, cols = input.shape if input.ndim != 1 else (input.shape[0], 1)
    assert (
        input.ndim == 2 or input.ndim == 1
    ), f"Input matrix is dimension '{input.ndim}'. Expected 2D matrix or 1D vector!"

    m = Float64MultiArray()
    m.layout.data_offset = 0
    m.layout.dim = [MultiArrayDimension(), MultiArrayDimension()]
    m.layout.dim[0].label = "rows"
    m.layout.dim[0].size = rows
    m.layout.dim[0].stride = input.size
    m.layout.dim[1].label = "cols"
    m.layout.dim[1].stride = cols
    m.layout.dim[1].size = cols
    # Flatten the matrix to a vector
    m.data = input.reshape(-1).tolist()
    return m


def matrix_msg_to_numpy(
    msg: Float64MultiArray, return_vector: bool = True
) -> npt.NDArray[np.float64]:
    """Converts ROS array message into numpy array.

    Args:
        msg (std_msgs.msg.Float64MultiArray): Input ROS message with array.
        return_vector (bool, optional): If ``True`` vector is returned in a shape (N,)
        otherwise the shape is (N,1). Defaults to True.

    Returns:
        npt.NDArray[np.float64]: Output numpy matrix.
    """
    assert len(msg.layout.dim) == 2, "The ROS message must be a 2D matrix!"
    if return_vector and msg.layout.dim[1].size == 1:
        return np.array(msg.data)
    return np.array(msg.data).reshape(msg.layout.dim[0].size, msg.layout.dim[1].size)


def joint_state_msg_to_numpy(msg: JointState) -> lfc_py_types.JointState:
    """Converts ROS JointState message into internal LFC JointState class.

    Args:
        msg (sensor_msgs.msg.JointState): Input ROS message.

    Returns:
        lfc_py_types.JointState: Output LFC representation of JointState.
    """
    return lfc_py_types.JointState(
        name=msg.name,
        position=np.array(msg.position),
        velocity=np.array(msg.velocity),
        effort=np.array(msg.effort),
    )


def contact_msg_to_numpy(msg: Contact) -> lfc_py_types.Contact:
    """Converts ROS Contact message into internal LFC Contact class.

    Args:
        msg (linear_feedback_controller_msgs.msg.Contact): Input ROS message.

    Returns:
        lfc_py_types.Contact: Output LFC representation of Contact.
    """
    return lfc_py_types.Contact(
        active=msg.active,
        name=msg.name,
        wrench=wrench_msg_to_numpy(msg.wrench),
        pose=pose_msg_to_numpy(msg.pose),
    )


def sensor_msg_to_numpy(msg: Sensor) -> lfc_py_types.Sensor:
    """Converts ROS Sensor message into internal LFC Sensor class.

    Args:
        msg (linear_feedback_controller_msgs.msg.Sensor): Input ROS message.

    Returns:
        lfc_py_types.Sensor: Output LFC representation of Sensor.
    """
    return lfc_py_types.Sensor(
        base_pose=pose_msg_to_numpy(msg.base_pose),
        base_twist=twist_msg_to_numpy(msg.base_twist),
        joint_state=joint_state_msg_to_numpy(msg.joint_state),
        contacts=[contact_msg_to_numpy(contact) for contact in msg.contacts],
    )


def control_msg_to_numpy(msg: Control) -> lfc_py_types.Control:
    """Converts ROS Control message into internal LFC Control class.

    Args:
        msg (linear_feedback_controller_msgs.msg.Control): Input ROS message.

    Returns:
        lfc_py_types.Control: Output LFC representation of Control.
    """
    return lfc_py_types.Control(
        feedback_gain=matrix_msg_to_numpy(msg.feedback_gain),
        feedforward=matrix_msg_to_numpy(msg.feedforward),
        initial_state=sensor_msg_to_numpy(msg.initial_state),
    )


def joint_state_numpy_to_msg(input: lfc_py_types.JointState) -> JointState:
    """Converts internal LFC JointState class into ROS JointState message.

    Args:
        input (lfc_py_types.JointState): Input LFC representation of Control.

    Returns:
        sensor_msgs.msg.JointState: Output ROS message.
    """
    return JointState(
        name=input.name,
        position=input.position,
        velocity=input.velocity,
        effort=input.effort,
    )


def contact_numpy_to_msg(input: lfc_py_types.Contact) -> Contact:
    """Converts internal LFC Contact class into ROS Contact message.

    Args:
        input (lfc_py_types.Contact): Input LFC representation of Control.

    Returns:
        linear_feedback_controller_msgs.msg.Contact: Output ROS message.
    """
    return Contact(
        active=input.active,
        name=input.name,
        wrench=wrench_numpy_to_msg(input.wrench),
        pose=pose_numpy_to_msg(input.pose),
    )


def sensor_numpy_to_msg(input: lfc_py_types.Sensor) -> Sensor:
    """Converts internal LFC Sensor class into ROS Sensor message.

    Args:
        input (lfc_py_types.Sensor): Input LFC representation of Control.

    Returns:
        linear_feedback_controller_msgs.msg.Sensor: Output ROS message.
    """
    return Sensor(
        base_pose=pose_numpy_to_msg(input.base_pose),
        base_twist=twist_numpy_to_msg(input.base_twist),
        joint_state=joint_state_numpy_to_msg(input.joint_state),
        contacts=[contact_numpy_to_msg(contact) for contact in input.contacts],
    )


def control_numpy_to_msg(input: lfc_py_types.Control) -> Control:
    """Converts internal LFC Control class into ROS Control message.

    Args:
        input (lfc_py_types.Control): Input LFC representation of Control.

    Returns:
        linear_feedback_controller_msgs.msg.Control: Output ROS message.
    """
    return Control(
        feedback_gain=matrix_numpy_to_msg(input.feedback_gain),
        feedforward=matrix_numpy_to_msg(input.feedforward),
        initial_state=sensor_numpy_to_msg(input.initial_state),
    )
