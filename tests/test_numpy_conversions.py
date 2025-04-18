#!/usr/bin/env python

import numpy as np
from copy import deepcopy
from rclpy.time import Time
from builtin_interfaces.msg import Time as TimeMsg

from linear_feedback_controller_msgs_py.numpy_conversions import *
import linear_feedback_controller_msgs_py.lfc_py_types as lfc_py_types


def test_check_numpy_constructors() -> None:
    joint_state = lfc_py_types.JointState(
        name=["joint_0", "joint_1"],
        position=np.array([1.0, 1.0]),
        velocity=np.array([1.0, 1.0]),
        effort=np.array([1.0, 1.0]),
    )
    contact = lfc_py_types.Contact(
        active=False,
        name="contact_0",
        wrench=np.ones(6),
        pose=np.ones(7),
    )
    # Test the Sensor and Control constructor with and without stamp for backward compatibility
    sensor = lfc_py_types.Sensor(
        base_pose=np.ones(7),
        base_twist=np.ones(6),
        joint_state=joint_state,
        contacts=[contact],
        stamp=Time(),
    )
    lfc_py_types.Control(
        feedback_gain=np.ones((4, 4)),
        feedforward=np.ones(4),
        initial_state=sensor,
        stamp=Time(),
    )

    sensor = lfc_py_types.Sensor(
        base_pose=np.ones(7),
        base_twist=np.ones(6),
        joint_state=joint_state,
        contacts=[contact],
    )
    lfc_py_types.Control(
        feedback_gain=np.ones((4, 4)),
        feedforward=np.ones(4),
        initial_state=sensor,
    )


def test_check_ros_numpy_matrix_conversion() -> None:
    numpy_random_matrix = np.random.rand(5, 6)

    ros_matrix = matrix_numpy_to_msg(deepcopy(numpy_random_matrix))
    numpy_back_converted_matrix = matrix_msg_to_numpy(ros_matrix)

    np.testing.assert_array_equal(
        numpy_back_converted_matrix,
        numpy_random_matrix,
        err_msg="Matrix after conversion back to "
        + "Numpy is not equal the initial matrix!",
    )

    numpy_random_vector = np.random.rand(20)

    ros_vector = matrix_numpy_to_msg(deepcopy(numpy_random_vector))

    for return_vector in (True, False):
        numpy_back_converted_vector = matrix_msg_to_numpy(ros_vector, return_vector)

        np.testing.assert_array_equal(
            numpy_back_converted_vector,
            (
                numpy_random_vector
                if return_vector
                else numpy_random_vector.reshape(-1, 1)
            ),
            err_msg="Vector after conversion back to "
            + "Numpy is not equal the initial vector "
            + f"for case with 'return_vector={return_vector}'",
        )


def test_check_ros_numpy_joint_state_conversion() -> None:
    numpy_joint_state = lfc_py_types.JointState(
        name=["1", "2", "3", "4", "5", "6"],
        position=np.random.rand(6),
        velocity=np.random.rand(6),
        effort=np.random.rand(6),
    )

    # Pass deep copy to ensure memory is separate
    ros_joint_state = joint_state_numpy_to_msg(deepcopy(numpy_joint_state))
    numpy_back_converted_join_state = joint_state_msg_to_numpy(ros_joint_state)

    assert (
        numpy_joint_state.name == numpy_back_converted_join_state.name
    ), "Names after conversion back to Numpy is not equal initial values!"

    np.testing.assert_array_equal(
        numpy_joint_state.position,
        numpy_back_converted_join_state.position,
        err_msg="Positions after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_joint_state.velocity,
        numpy_back_converted_join_state.velocity,
        err_msg="Velocities after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_joint_state.effort,
        numpy_back_converted_join_state.effort,
        err_msg="Efforts after conversion back to "
        + "Numpy is not equal initial values!",
    )


def test_check_ros_numpy_control_conversion() -> None:
    quat = np.random.rand(4)
    quat = quat / np.linalg.norm(quat)

    numpy_control = lfc_py_types.Control(
        initial_state=lfc_py_types.Sensor(
            base_pose=np.concatenate((np.random.rand(3), quat)),
            base_twist=np.random.rand(6),
            joint_state=lfc_py_types.JointState(
                name=["1", "2", "3", "4", "5", "6"],
                position=np.random.rand(6),
                velocity=np.random.rand(6),
                effort=np.random.rand(6),
            ),
            contacts=[],
            stamp=Time.from_msg(TimeMsg(sec=np.random.randint(0, 100))),
        ),
        feedback_gain=np.random.rand(8, 4),
        feedforward=np.random.rand(4),
        stamp=Time.from_msg(TimeMsg(sec=np.random.randint(0, 100))),
    )

    ros_control_msg = control_numpy_to_msg(numpy_control)
    back_converted_numpy_control = control_msg_to_numpy(ros_control_msg)

    np.testing.assert_array_equal(
        numpy_control.initial_state.base_pose,
        back_converted_numpy_control.initial_state.base_pose,
        err_msg="Initial state base pose after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_control.initial_state.base_twist,
        back_converted_numpy_control.initial_state.base_twist,
        err_msg="Initial state base twist after conversion back to "
        + "Numpy is not equal initial values!",
    )

    assert (
        numpy_control.initial_state.joint_state.name
        == back_converted_numpy_control.initial_state.joint_state.name
    ), "Names after conversion back to Numpy is not equal initial values!"

    np.testing.assert_array_equal(
        numpy_control.initial_state.joint_state.position,
        back_converted_numpy_control.initial_state.joint_state.position,
        err_msg="Joint state position after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_control.initial_state.joint_state.velocity,
        back_converted_numpy_control.initial_state.joint_state.velocity,
        err_msg="Joint state velocity after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_control.initial_state.joint_state.effort,
        back_converted_numpy_control.initial_state.joint_state.effort,
        err_msg="Joint state effort after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_control.feedback_gain,
        back_converted_numpy_control.feedback_gain,
        err_msg="Feedback gains after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_control.feedforward,
        back_converted_numpy_control.feedforward,
        err_msg="Feed forward after conversion back to "
        + "Numpy is not equal initial values!",
    )

    assert (
        numpy_control.stamp == back_converted_numpy_control.stamp
    ), "Control stamp conversion failed."

    assert (
        numpy_control.initial_state.stamp
        == back_converted_numpy_control.initial_state.stamp
    ), "Control initial state stamp conversion failed."


def test_check_ros_numpy_sensor_conversions() -> None:
    quat = np.random.rand(4)
    quat = quat / np.linalg.norm(quat)

    numpy_sensor = lfc_py_types.Sensor(
        base_pose=np.concatenate((np.random.rand(3), quat)),
        base_twist=np.random.rand(6),
        joint_state=lfc_py_types.JointState(
            name=["1", "2", "3", "4", "5", "6"],
            position=np.random.rand(6),
            velocity=np.random.rand(6),
            effort=np.random.rand(6),
        ),
        contacts=[],
        # Note that we have to create the time using a Time message to set the clock type
        # of the C++ rcl Time to ROS_TIME.
        stamp=Time.from_msg(TimeMsg(sec=np.random.randint(0, 100))),
    )

    numpy_sensor.contacts.append(
        lfc_py_types.Contact(
            active=True,
            name="left_foot",
            wrench=np.random.rand(6),
            pose=np.random.rand(7),
        )
    )

    numpy_sensor.contacts.append(
        lfc_py_types.Contact(
            active=False,
            name="right_foot",
            wrench=np.random.rand(6),
            pose=np.random.rand(7),
        )
    )

    ros_sensor = sensor_numpy_to_msg(numpy_sensor)
    numpy_back_converted_sensor = sensor_msg_to_numpy(ros_sensor)

    np.testing.assert_array_equal(
        numpy_sensor.base_pose,
        numpy_back_converted_sensor.base_pose,
        err_msg="Base Pose after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_sensor.base_twist,
        numpy_back_converted_sensor.base_twist,
        err_msg="Base Twist after conversion back to "
        + "Numpy is not equal initial values!",
    )

    assert (
        numpy_sensor.joint_state.name == numpy_back_converted_sensor.joint_state.name
    ), "Joint names after conversion back to Numpy is not equal initial values!"

    np.testing.assert_array_equal(
        numpy_sensor.joint_state.position,
        numpy_back_converted_sensor.joint_state.position,
        err_msg="Joint positions after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_sensor.joint_state.velocity,
        numpy_back_converted_sensor.joint_state.velocity,
        err_msg="Joint velocities after conversion back to "
        + "Numpy is not equal initial values!",
    )

    np.testing.assert_array_equal(
        numpy_sensor.joint_state.effort,
        numpy_back_converted_sensor.joint_state.effort,
        err_msg="Joint efforts after conversion back to "
        + "Numpy is not equal initial values!",
    )

    assert (
        numpy_sensor.stamp == numpy_back_converted_sensor.stamp
    ), "Sensor stamp conversion failed."

    assert len(numpy_sensor.contacts) == len(
        numpy_back_converted_sensor.contacts
    ), "Number of contacts after conversion doesn't match number of contacts before conversion!"

    for i in range(len(numpy_sensor.contacts)):
        c1 = numpy_sensor.contacts[i]
        c2 = numpy_back_converted_sensor.contacts[i]
        assert (
            c1.active == c2.active
        ), f"Active parameter before and after conversion differs at index '{i}'"
        assert (
            c1.name == c2.name
        ), f"Name parameter before and after conversion differs at index '{i}'"

        np.testing.assert_array_equal(
            c1.wrench,
            c2.wrench,
            err_msg=f"Wrench parameter before and after conversion differs at index '{i}'",
        )

        np.testing.assert_array_equal(
            c1.pose,
            c2.pose,
            err_msg=f"Pose parameter before and after conversion differs at index '{i}'",
        )
