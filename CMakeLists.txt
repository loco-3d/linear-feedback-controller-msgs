cmake_minimum_required(VERSION 3.22.1)

set(PROJECT_NAME linear_feedback_controller_msgs)
set(PROJECT_DESCRIPTION "ROS messages for LFC")
set(PROJECT_URL "http://github.com/loco-3d/linear-feedback-controller-msgs")

find_package(jrl-cmakemodules QUIET CONFIG)
if(jrl-cmakemodules_FOUND)
  message(STATUS "JRL cmakemodules found on system at ${JRL_CMAKE_MODULES}")
  get_property(
    JRL_CMAKE_MODULES
    TARGET jrl-cmakemodules::jrl-cmakemodules
    PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
else()
  message(STATUS "JRL cmakemodules not found. Let's fetch it.")
  include(FetchContent)
  FetchContent_Declare(
    "jrl-cmakemodules"
    GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
  FetchContent_MakeAvailable("jrl-cmakemodules")
  FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
endif()
include("${JRL_CMAKE_MODULES}/base.cmake")
compute_project_args(PROJECT_ARGS LANGUAGES C CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

find_package(Eigen3 REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(
  ${PROJECT_NAME}
  "msg/Contact.msg"
  "msg/Control.msg"
  "msg/Sensor.msg"
  DEPENDENCIES
  builtin_interfaces
  std_msgs
  sensor_msgs
  geometry_msgs
  ADD_LINTER_TESTS)
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME}
                              rosidl_typesupport_cpp)

#
# Main lib.
#
set(${PROJECT_NAME}_HEADERS include/${PROJECT_NAME}/eigen_conversions.hpp)
set(${PROJECT_NAME}_SOURCES "")
add_library(${PROJECT_NAME}_conversion INTERFACE)
target_link_libraries(
  ${PROJECT_NAME}_conversion INTERFACE Eigen3::Eigen tf2_eigen::tf2_eigen
                                       "${cpp_typesupport_target}")
target_include_directories(
  ${PROJECT_NAME}_conversion
  INTERFACE $<INSTALL_INTERFACE:include/>
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)

#
# Unit tests
#
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_eigen_conversions tests/test_eigen_conversions.cpp
                  tests/gtest_main.cpp)
  target_link_libraries(test_eigen_conversions ${PROJECT_NAME}_conversion)
  set_tests_properties(
    test_eigen_conversions
    PROPERTIES ENVIRONMENT_MODIFICATION
               LD_LIBRARY_PATH=path_list_prepend:${CMAKE_CURRENT_BINARY_DIR})

  find_package(ament_cmake_pytest REQUIRED)
  set(_pytest_tests tests/test_numpy_conversions.py)
  foreach(_test_path ${_pytest_tests})
    get_filename_component(_test_name ${_test_path} NAME_WE)
    ament_add_pytest_test(
      ${_test_name}
      ${_test_path}
      APPEND_ENV
      PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_py
      TIMEOUT
      60
      WORKING_DIRECTORY
      ${CMAKE_SOURCE_DIR})
  endforeach()
endif()

#
# Install
#

# Install Python modules
ament_python_install_package(${PROJECT_NAME}_py)

install(
  TARGETS ${PROJECT_NAME}_conversion
  EXPORT export_${PROJECT_NAME}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(
  DIRECTORY include/${PROJECT_NAME}
  DESTINATION include
  PATTERN "third_party" EXCLUDE)

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(rosidl_default_runtime)
ament_export_dependencies(eigen3_cmake_module)
ament_export_dependencies(Eigen3)
ament_export_dependencies(tf2_eigen)

ament_package()
