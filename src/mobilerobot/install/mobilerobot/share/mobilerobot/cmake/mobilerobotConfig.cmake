# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_mobilerobot_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED mobilerobot_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(mobilerobot_FOUND FALSE)
  elseif(NOT mobilerobot_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(mobilerobot_FOUND FALSE)
  endif()
  return()
endif()
set(_mobilerobot_CONFIG_INCLUDED TRUE)

# output package information
if(NOT mobilerobot_FIND_QUIETLY)
  message(STATUS "Found mobilerobot: 0.0.0 (${mobilerobot_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'mobilerobot' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${mobilerobot_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(mobilerobot_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${mobilerobot_DIR}/${_extra}")
endforeach()
