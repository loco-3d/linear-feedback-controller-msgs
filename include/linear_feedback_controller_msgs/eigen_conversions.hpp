#ifndef ROS_WBMPC_MSGS_ROS_EIGEN_CONVERSION_HPP
#define ROS_WBMPC_MSGS_ROS_EIGEN_CONVERSION_HPP

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <linear_feedback_controller_msgs/msg/control.hpp>
#include <linear_feedback_controller_msgs/msg/sensor.hpp>
#include <tf2_eigen/tf2_eigen.hpp>

namespace linear_feedback_controller_msgs {

namespace Eigen {

struct JointState {
  std::vector<std::string> name;
  ::Eigen::VectorXd position;
  ::Eigen::VectorXd velocity;
  ::Eigen::VectorXd effort;
};

struct Contact {
  bool active;
  std::string name;
  ::Eigen::Matrix<double, 6, 1> wrench;
  ::Eigen::Matrix<double, 7, 1> pose;
};

struct Sensor {
  ::Eigen::Matrix<double, 7, 1> base_pose;
  ::Eigen::Matrix<double, 6, 1> base_twist;
  JointState joint_state;
  std::vector<Contact> contacts;
};

struct Control {
  ::Eigen::MatrixXd feedback_gain;
  ::Eigen::VectorXd feedforward;
  linear_feedback_controller_msgs::Eigen::Sensor initial_state;
};
}  // namespace Eigen

// Create an alias to use only one namespace here.
inline void wrenchEigenToMsg(const ::Eigen::Matrix<double, 6, 1>& e,
                             geometry_msgs::msg::Wrench& m) {
  tf2::toMsg(e.template head<3>(), m.force);
  tf2::toMsg(e.template tail<3>(), m.torque);
}

inline void wrenchMsgToEigen(const geometry_msgs::msg::Wrench& m,
                             ::Eigen::Matrix<double, 6, 1>& e) {
  e(0) = m.force.x;
  e(1) = m.force.y;
  e(2) = m.force.z;
  e(3) = m.torque.x;
  e(4) = m.torque.y;
  e(5) = m.torque.z;
}

// Create an alias to use only one namespace here.
template <class Derived>
inline void matrixEigenToMsg(const ::Eigen::MatrixBase<Derived>& e,
                             std_msgs::msg::Float64MultiArray& m) {
  // verify the input object.
  m.layout.data_offset = 0;
  m.layout.dim.resize(2);
  m.layout.dim[0].label = "rows";
  m.layout.dim[0].size = e.rows();
  m.layout.dim[0].stride = e.size();
  m.layout.dim[1].label = "cols";
  m.layout.dim[1].stride = e.cols();
  m.layout.dim[1].size = e.cols();
  m.data.resize(m.layout.dim[0].stride, 0.0);

  for (int i = 0; i < e.rows(); ++i) {
    for (int j = 0; j < e.cols(); ++j) {
      m.data[m.layout.data_offset + m.layout.dim[1].stride * i + j] = e(i, j);
    }
  }
}

template <class Derived>
inline void matrixMsgToEigen(const std_msgs::msg::Float64MultiArray& m,
                             ::Eigen::MatrixBase<Derived>& e) {
  assert(m.layout.dim.size() == 2 && "The ROS message must be a 2D matrix.");

  // verify the input object.
  assert(m.layout.dim[0].stride == e.size() &&
         "Input and output size do not match.");
  assert(m.layout.dim[0].size == e.rows() &&
         "Input and output size do not match.");
  assert(m.layout.dim[1].stride == e.cols() &&
         "Input and output size do not match.");
  assert(m.layout.dim[1].size == e.cols() &&
         "Input and output size do not match.");

  for (int i = 0; i < e.rows(); ++i) {
    for (int j = 0; j < e.cols(); ++j) {
      e(i, j) = m.data[m.layout.data_offset + m.layout.dim[1].stride * i + j];
    }
  }
}

/**
 * Msg To Eigen.
 */

inline void jointStateMsgToEigen(
    const sensor_msgs::msg::JointState& m,
    linear_feedback_controller_msgs::Eigen::JointState& e) {
  e.name = m.name;
  e.position = ::Eigen::Map<const ::Eigen::VectorXd>(m.position.data(),
                                                     m.position.size());
  e.velocity = ::Eigen::Map<const ::Eigen::VectorXd>(m.velocity.data(),
                                                     m.velocity.size());
  e.effort =
      ::Eigen::Map<const ::Eigen::VectorXd>(m.effort.data(), m.effort.size());
}

inline void contactMsgToEigen(
    const linear_feedback_controller_msgs::msg::Contact& m,
    linear_feedback_controller_msgs::Eigen::Contact& e) {
  e.active = m.active;
  e.name = m.name;
  wrenchMsgToEigen(m.wrench, e.wrench);
  e.pose(0) = m.pose.position.x;
  e.pose(1) = m.pose.position.y;
  e.pose(2) = m.pose.position.z;
  e.pose(3) = m.pose.orientation.x;
  e.pose(4) = m.pose.orientation.y;
  e.pose(5) = m.pose.orientation.z;
  e.pose(6) = m.pose.orientation.w;
}

inline void sensorMsgToEigen(
    const linear_feedback_controller_msgs::msg::Sensor& m,
    linear_feedback_controller_msgs::Eigen::Sensor& e) {
  e.base_pose(0) = m.base_pose.position.x;
  e.base_pose(1) = m.base_pose.position.y;
  e.base_pose(2) = m.base_pose.position.z;
  e.base_pose(3) = m.base_pose.orientation.x;
  e.base_pose(4) = m.base_pose.orientation.y;
  e.base_pose(5) = m.base_pose.orientation.z;
  e.base_pose(6) = m.base_pose.orientation.w;
  tf2::fromMsg(m.base_twist, e.base_twist);
  jointStateMsgToEigen(m.joint_state, e.joint_state);
  e.contacts.resize(m.contacts.size());
  for (std::size_t i = 0; i < m.contacts.size(); ++i) {
    contactMsgToEigen(m.contacts[i], e.contacts[i]);
  }
}

inline void controlMsgToEigen(
    const linear_feedback_controller_msgs::msg::Control& m,
    linear_feedback_controller_msgs::Eigen::Control& e) {
  matrixMsgToEigen(m.feedback_gain, e.feedback_gain);
  matrixMsgToEigen(m.feedforward, e.feedforward);
  sensorMsgToEigen(m.initial_state, e.initial_state);
}

/**
 * Eigen To Msg.
 */

inline void jointStateEigenToMsg(
    const linear_feedback_controller_msgs::Eigen::JointState& e,
    sensor_msgs::msg::JointState& m) {
  m.name = e.name;
  m.position = std::vector<double>(e.position.data(),
                                   e.position.data() + e.position.size());
  m.velocity = std::vector<double>(e.velocity.data(),
                                   e.velocity.data() + e.velocity.size());
  m.effort =
      std::vector<double>(e.effort.data(), e.effort.data() + e.effort.size());
}

inline void contactEigenToMsg(
    const linear_feedback_controller_msgs::Eigen::Contact& e,
    linear_feedback_controller_msgs::msg::Contact& m) {
  m.active = e.active;
  m.name = e.name;
  wrenchEigenToMsg(e.wrench, m.wrench);
  m.pose.position.x = e.pose(0);
  m.pose.position.y = e.pose(1);
  m.pose.position.z = e.pose(2);
  m.pose.orientation.x = e.pose(3);
  m.pose.orientation.y = e.pose(4);
  m.pose.orientation.z = e.pose(5);
  m.pose.orientation.w = e.pose(6);
}

inline void sensorEigenToMsg(
    const linear_feedback_controller_msgs::Eigen::Sensor e,
    linear_feedback_controller_msgs::msg::Sensor& m) {
  m.base_pose.position.x = e.base_pose(0);
  m.base_pose.position.y = e.base_pose(1);
  m.base_pose.position.z = e.base_pose(2);
  m.base_pose.orientation.x = e.base_pose(3);
  m.base_pose.orientation.y = e.base_pose(4);
  m.base_pose.orientation.z = e.base_pose(5);
  m.base_pose.orientation.w = e.base_pose(6);
  m.base_twist = tf2::toMsg(e.base_twist);
  jointStateEigenToMsg(e.joint_state, m.joint_state);
  m.contacts.resize(e.contacts.size());
  for (std::size_t i = 0; i < e.contacts.size(); ++i) {
    contactEigenToMsg(e.contacts[i], m.contacts[i]);
  }
}

inline void controlEigenToMsg(
    const linear_feedback_controller_msgs::Eigen::Control& e,
    linear_feedback_controller_msgs::msg::Control& m) {
  matrixEigenToMsg(e.feedback_gain, m.feedback_gain);
  matrixEigenToMsg(e.feedforward, m.feedforward);
  sensorEigenToMsg(e.initial_state, m.initial_state);
}

}  // namespace linear_feedback_controller_msgs

#endif  // ROS_WBMPC_MSGS_ROS_EIGEN_CONVERSION_HPP
