cmake_minimum_required(VERSION 3.22.1)

project(linear_feedback_controller_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Require for _conversion
find_package(Eigen3 REQUIRED)
find_package(tf2_eigen REQUIRED)

# Require by msg
find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Contact.msg"
  "msg/Control.msg"
  "msg/Sensor.msg"
  DEPENDENCIES builtin_interfaces std_msgs sensor_msgs geometry_msgs
  ADD_LINTER_TESTS
)

#
# Unit tests
#
if(BUILD_TESTING)
  # CPP
  ament_add_gtest(test_${PROJECT_NAME}_conversions
    tests/test_eigen_conversions.cpp
    tests/gtest_main.cpp
  )

  target_include_directories(test_${PROJECT_NAME}_conversions
    PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  )

  rosidl_get_typesupport_target(cpp_typesupport_target
    ${PROJECT_NAME} "rosidl_typesupport_cpp"
  )

  target_link_libraries(test_${PROJECT_NAME}_conversions
    Eigen3::Eigen
    tf2_eigen::tf2_eigen
    "${cpp_typesupport_target}"
  )

  # PYTHON
  find_package(ament_cmake_pytest REQUIRED)
  set(_pytest_tests
    tests/test_numpy_conversions.py
  )
  foreach(_test_path ${_pytest_tests})
    get_filename_component(_test_name ${_test_path} NAME_WE)
    ament_add_pytest_test(${_test_name} ${_test_path}
      APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_py
      TIMEOUT 60
      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
  endforeach()
endif()

#
# Install
#

include(GNUInstallDirs)

# Install Python modules
ament_python_install_package(${PROJECT_NAME}_py)

install(DIRECTORY include/${PROJECT_NAME}
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}
)

install(FILES package.xml DESTINATION share/${PROJECT_NAME})

ament_export_include_directories(include)
ament_export_dependencies(rosidl_default_runtime)
ament_export_dependencies(eigen3_cmake_module)
ament_export_dependencies(Eigen3)
ament_export_dependencies(tf2_eigen)

ament_package()
